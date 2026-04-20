# -*- coding: utf-8 -*-
"""
TikTok Scraper — v3.1
=====================================================
Lisans Tezi: "TikTok'ta Etkili Marka İş Birliği için İçerik Üreticisi
              Seçiminin Optimizasyonu"
Eskişehir Teknik Üniversitesi — Endüstri Mühendisliği

v3.1 YENİLİKLERİ (v3.0 üzerine):
  1. Driver otomatik kurtarma: Chrome crash / uyku sonrası "invalid session id"
     hatası alındığında driver kapatılıp yeniden başlatılır, sayfa tekrar yüklenir.
  2. is_driver_alive() yardımcı fonksiyonu eklendi.
  3. smart_get() InvalidSessionIdException yakalar → driver yeniden başlatılır.
  4. Ana döngüde try/except ile beklenmedik driver hatalarına karşı ek güvence.
  5. Sistem uykuya geçmesin diye macOS / Linux için caffeinate / systemd-inhibit
     uyarısı başlangıçta gösterilir.

v3.0 YENİLİKLERİ (v2.0 üzerine):
  1. Profil ekran görüntüsü sistemi tamamen yenilendi:
     - screenshots/full/   → tam sayfa ekran görüntüsü
     - screenshots/cropped/ → profil header bölgesi (fotoğraf + isim + istatistikler)
  2. Header crop: önce DOM'dan getBoundingClientRect() ile kesin konum,
     bulunamazsa CROP_TOP_PADDING / CROP_BOTTOM_PADDING sabit değerleriyle fallback.
  3. Video sayfalarında ss alma KALDIRILDI — sadece profil ss'leri alınır.
  4. save_debug() sadece hata/debug için raw HTML kaydeder.
  5. Pillow bağımlılığı eklendi (pip install pillow).

v2.0 DÜZELTMELERİ (korundu):
  1. views = NaN sorunu   → 8 katmanlı CSS + JavaScript fallback seçici zinciri
  2. caption = None sorunu → 6 katmanlı CSS + JS innerHTML fallback
  3. Followers doğrulama  → Scraping sonrası mantık kontrolü + uyarı bayrağı
  4. Yayın sıklığı        → last_post_days_ago: son video ile bugün arası gün
  5. Sponsorlu içerik tespiti → caption içinde #ad #sponsored #işbirliği tarama
  6. Video seçici güncelleme → TikTok Mart 2025 DOM yapısına göre
  7. Profil yeniden deneme → followers=0 veya hatalı görünüyorsa 1 kez retry
  8. Kategorilendirme     → caption/hashtag boş gelirse bio'ya ağırlık artırıldı

ÇIKTILAR:
  data_tiktok/profiles.csv
  data_tiktok/videos.csv
  data_tiktok/tiktok_profiles.xlsx
  data_tiktok/tiktok_videos.xlsx
  data_tiktok/tiktok_profiles_categorized.xlsx
  data_tiktok/tiktok_videos_categorized.xlsx
  data_tiktok/raw_html/...
  data_tiktok/screenshots/full/...        ← YENİ: tam ekran görüntüleri
  data_tiktok/screenshots/cropped/...     ← YENİ: kırpılmış header görüntüleri
  data_tiktok/run_state.json

GEREKLİ PAKETLER:
  pip install selenium webdriver-manager pandas numpy openpyxl pillow
"""

import csv
import io
import json
import re
import time
import random
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException

from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings("ignore")


# =====================================================================
# YAPILANDIRMA
# =====================================================================

DATA_DIR       = Path("data_tiktok")
RAW_HTML_DIR   = DATA_DIR / "raw_html"
SHOT_DIR       = DATA_DIR / "screenshots"
SHOT_FULL_DIR  = SHOT_DIR / "full"      # ← v3: tam ekran görüntüleri
SHOT_CROP_DIR  = SHOT_DIR / "cropped"   # ← v3: kırpılmış header görüntüleri
STATE_FILE     = DATA_DIR / "run_state.json"
PROFILES_CSV   = DATA_DIR / "profiles.csv"
VIDEOS_CSV     = DATA_DIR / "videos.csv"
TXT_FILE       = Path("tiktok_kullanicilar.txt")

MAX_VIDEOS_PER_PROFILE  = 10
PROFILE_SCROLL_STEPS    = 8
SLEEP_BETWEEN_PROFILES  = (5.0, 9.0)
SLEEP_BETWEEN_VIDEOS    = (3.0, 6.0)

HEADLESS           = False
CHROME_PROFILE_DIR = Path("chrome_profile").resolve()
PAGE_WAIT_SEC      = 25
CHALLENGE_WAIT_SEC = 20 * 60
NAV_RETRIES        = 3

FOLLOWERS_SANITY_MIN          = 100
CATEGORY_CONFIDENCE_THRESHOLD = 20

# ── v3.2: Profil header crop — DİNAMİK (DOM tabanlı) ───────────────
# Kırpma stratejisi (öncelik sırasıyla):
#   1. Sayfadaki profil container elementinin gerçek yüksekliği (en doğru)
#   2. Bulunamazsa: tam genişlik, üstten HEADER_FALLBACK_HEIGHT px yükseklik
#
# HEADER_EXTRA_BOTTOM: DOM'dan bulunan alt sınıra eklenecek nefes boşluğu (px)
# HEADER_FALLBACK_HEIGHT: DOM bulunamazsa alınacak yükseklik (px)
HEADER_EXTRA_BOTTOM    = 60    # header'ın altına biraz boşluk
HEADER_FALLBACK_HEIGHT = 420   # fallback yüksekliği — gerekirse artırın

# Profil container'ını bulmak için denenen CSS seçiciler (sırayla)
HEADER_CROP_SELECTORS = [
    '[data-e2e="user-page"]',
    '[class*="DivShareLayoutHeader"]',
    '[class*="share-layout-header"]',
    '[class*="ShareLayoutHeader"]',
    'h1[data-e2e="user-title"]',
    'strong[data-e2e="followers-count"]',
]
# ────────────────────────────────────────────────────────────────────

DATA_DIR.mkdir(exist_ok=True)
RAW_HTML_DIR.mkdir(exist_ok=True)
SHOT_FULL_DIR.mkdir(parents=True, exist_ok=True)
SHOT_CROP_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================================
# CSV SÜTUN TANIMLAMALARI
# =====================================================================

PROFILE_FIELDS = [
    "normalized_username",
    "profile_url",
    "username",
    "display_name",
    "bio",
    "followers",
    "following",
    "likes",
    "website_url",
    "followers_suspicious",
    "post_count_visible",
    "last_post_days_ago",
    "avg_video_likes_profile",
    "debug_html_path",
    "screenshot_full_path",     # ← v3: tam ekran görüntüsü yolu
    "screenshot_cropped_path",  # ← v3: kırpılmış header yolu
    "error",
]

VIDEO_FIELDS = [
    "profile_username",
    "video_url",
    "video_rank_on_profile",
    "is_pinned",
    "caption",
    "hashtags",
    "hashtag_count",
    "music_text",
    "posted_at_raw",
    "posted_at_iso",
    "video_duration_sec",
    "views",
    "video_likes",
    "comments",
    "shares",
    "like_rate",
    "engagement_rate",
    "comments_enabled",
    "comments_disabled_reason",
    "is_sponsored",
    "sponsored_tag",
    "caption_source",
    "views_source",
    "debug_html_path",
    "error",
]


# =====================================================================
# YARDIMCI FONKSİYONLAR
# =====================================================================

def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def jitter_sleep(a_b: Tuple[float, float]):
    time.sleep(random.uniform(a_b[0], a_b[1]))

def safe_filename(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_\-\.]+", "_", s)
    return s[:180]

def normalize_username(raw: str) -> str:
    s = raw.strip()
    if "tiktok.com" in s:
        m = re.search(r"@([^/?&#]+)", s)
        if m:
            return m.group(1).lower()
    return s.lstrip("@").lower()

def get_profile_url(username_or_url: str) -> str:
    raw = username_or_url.strip()
    if raw.startswith("http"):
        return raw
    u = normalize_username(raw)
    return f"https://www.tiktok.com/@{u}"

def parse_number(text: Optional[str]) -> Optional[int]:
    """K / M / B kısaltmalarını tam sayıya çevirir."""
    if not text:
        return None
    t = text.strip().upper().replace(",", "").replace(" ", "")
    if not t:
        return None
    mult = 1
    if t.endswith("K"):
        mult = 1_000;         t = t[:-1]
    elif t.endswith("M"):
        mult = 1_000_000;     t = t[:-1]
    elif t.endswith("B"):
        mult = 1_000_000_000; t = t[:-1]
    try:
        return int(float(t) * mult)
    except ValueError:
        return None

def save_debug_html(driver, tag: str) -> str:
    """Sadece ham HTML kaydeder (hata durumlarında debug için)."""
    html_path = RAW_HTML_DIR / f"{safe_filename(tag)}_{ts()}.html"
    try:
        html_path.write_text(driver.page_source, encoding="utf-8")
    except Exception:
        pass
    return str(html_path)

# v2 uyumluluğu için eski imza korunur — video hata durumlarında kullanılır
def save_debug(driver, tag: str) -> Tuple[str, str]:
    """HTML debug kaydeder; video hata yolları için."""
    html_path = RAW_HTML_DIR / f"{safe_filename(tag)}_{ts()}.html"
    try:
        html_path.write_text(driver.page_source, encoding="utf-8")
    except Exception:
        pass
    return str(html_path), ""

def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"done_users": [], "done_videos": []}

def save_state(state: Dict[str, Any]):
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

def append_csv_fixed(path: Path, fields: List[str], row: Dict[str, Any]):
    is_new = not path.exists()
    out = {k: row.get(k, None) for k in fields}
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=fields,
            extrasaction="ignore",
            quoting=csv.QUOTE_ALL,
            escapechar="\\",
        )
        if is_new:
            writer.writeheader()
        writer.writerow(out)

def wait_any(driver, css_list: List[str], timeout: int) -> Optional[str]:
    end = time.time() + timeout
    while time.time() < end:
        for css in css_list:
            try:
                if driver.find_elements(By.CSS_SELECTOR, css):
                    return css
            except Exception:
                pass
        time.sleep(0.4)
    return None

def text_or_none(driver, css: str) -> Optional[str]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, css)
        t  = el.text.strip()
        return t if t else None
    except Exception:
        return None

def attr_or_none(driver, css: str, attr: str) -> Optional[str]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, css)
        v  = el.get_attribute(attr)
        return v.strip() if v else None
    except Exception:
        return None

def extract_hashtags(caption: Optional[str]) -> List[str]:
    if not caption:
        return []
    return re.findall(r"#(\w+)", caption)

def try_parse_posted_at(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    s   = raw.strip()
    now = datetime.now()

    m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", s)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
        except Exception:
            pass

    m = re.search(r"\b(\d{1,2})-(\d{1,2})\b", s)
    if m:
        try:
            return datetime(now.year, int(m.group(1)), int(m.group(2))).isoformat()
        except Exception:
            pass

    patterns = [
        (r"\b(\d+)\s*(gün|day|days|d)\b",           "days"),
        (r"\b(\d+)\s*(saat|hour|hours|h)\b",         "hours"),
        (r"\b(\d+)\s*(dakika|minute|minutes|min)\b", "minutes"),
        (r"\b(\d+)\s*(hafta|week|weeks|w)\b",        "weeks"),
    ]
    for pat, unit in patterns:
        m = re.search(pat, s, re.IGNORECASE)
        if m:
            n = int(m.group(1))
            return (now - timedelta(**{unit: n})).isoformat()

    return None

def days_since(iso_str: Optional[str]) -> Optional[int]:
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(iso_str)
        return (datetime.now() - dt).days
    except Exception:
        return None


# =====================================================================
# SPONSORLU İÇERİK TESPİTİ
# =====================================================================

SPONSORED_TAGS = [
    "#ad", "#sponsored", "#reklam", "#işbirliği", "#isbirligi",
    "#partnership", "#collab", "#gifted", "#tanıtım", "#tanitim",
    "#promo", "#promotion", "paid partnership", "işbirliği içerir",
]

def detect_sponsored(caption: Optional[str]) -> Tuple[bool, Optional[str]]:
    if not caption:
        return False, None
    cap_lower = caption.lower()
    for tag in SPONSORED_TAGS:
        if tag in cap_lower:
            return True, tag
    return False, None


# =====================================================================
# CHALLENGE ALGILAMA
# =====================================================================

CHALLENGE_SELECTORS = [
    'iframe[src*="captcha"]',
    'iframe[title*="captcha"]',
    '[id*="captcha"]',
    '[class*="captcha"]',
    '[class*="verify"]',
    '[class*="verification"]',
    '[class*="CaptchaContainer"]',
]

PROFILE_EXPECTED = [
    'h1[data-e2e="user-title"]',
    'strong[data-e2e="followers-count"]',
    '[data-e2e="user-page"]',
]

VIDEO_EXPECTED = [
    'strong[data-e2e="like-count"]',
    '[data-e2e="browse-like-count"]',
    'strong[data-e2e="comment-count"]',
    '[data-e2e="comment-count"]',
    'a[href*="/music/"]',
    '[data-e2e="browse-music"]',
    'video',
]

def is_challenge(driver) -> bool:
    try:
        return wait_any(driver, CHALLENGE_SELECTORS, timeout=1) is not None
    except Exception:
        return False

def wait_challenge_clears(driver, context: str):
    print(f"\n[CAPTCHA] Challenge algılandı ({context}). "
          f"Tarayıcıda çöz, ardından otomatik devam eder.")
    save_debug_html(driver, f"challenge_{context}")
    end = time.time() + CHALLENGE_WAIT_SEC
    while time.time() < end:
        time.sleep(1.0)
        if not is_challenge(driver):
            print("[CAPTCHA] Çözüldü, devam ediliyor.")
            return
    print("[CAPTCHA] Süre doldu. ENTER → devam / Ctrl+C → çıkış.")
    input(">> ")


# =====================================================================
# AKILLI SAYFA GEZİNİMİ
# =====================================================================

def smart_get(driver, url: str, expected_css: List[str], context: str) -> Tuple[bool, webdriver.Chrome]:
    """
    Sayfayı yükler; başarıysa (True, driver), başarısızsa (False, driver) döner.
    Driver session ölmüşse otomatik olarak yeni driver başlatır ve döner.
    """
    for attempt in range(1, NAV_RETRIES + 1):
        # Her denemede önce session'ın canlı olup olmadığını kontrol et
        if not is_driver_alive(driver):
            driver = restart_driver(driver)

        try:
            driver.get(url)
        except (InvalidSessionIdException, WebDriverException) as e:
            msg = str(e).split("\n")[0]
            print(f"  [NAV] Driver hatası ({attempt}/{NAV_RETRIES}): {msg}")
            driver = restart_driver(driver)
            time.sleep(3)
            continue
        except Exception as e:
            print(f"  [NAV] driver.get hatası ({attempt}/{NAV_RETRIES}): {e}")
            time.sleep(3)
            continue

        time.sleep(2.0)
        hit = wait_any(driver, expected_css, timeout=PAGE_WAIT_SEC)
        if hit:
            return True, driver

        if is_challenge(driver):
            wait_challenge_clears(driver, context=context)
            if wait_any(driver, expected_css, timeout=PAGE_WAIT_SEC):
                return True, driver

        save_debug_html(driver, f"nav_fail_{context}_a{attempt}")
        time.sleep(3)

    return False, driver


# =====================================================================
# CHROME DRIVER
# =====================================================================

def create_driver() -> webdriver.Chrome:
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
    opts.add_argument("--profile-directory=Default")
    opts.add_argument("--lang=tr-TR")

    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service, options=opts)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"}
    )
    return driver


# =====================================================================
# v3.1: DRIVER SAĞLIK KONTROLÜ VE OTOMATİK KURTARMA
# =====================================================================

def is_driver_alive(driver) -> bool:
    """Driver session'ının hâlâ canlı olup olmadığını test eder."""
    try:
        _ = driver.current_url   # herhangi bir özelliğe erişmek yeterli
        return True
    except Exception:
        return False

def restart_driver(driver) -> webdriver.Chrome:
    """
    Mevcut driver'ı güvenle kapatır ve yeni bir tane başlatır.
    Çağrıldıktan sonra dönen yeni driver'ı kullanmaya devam et.
    """
    print("  [DRIVER] Session geçersiz — driver yeniden başlatılıyor...")
    try:
        driver.quit()
    except Exception:
        pass
    time.sleep(3)
    new_driver = create_driver()
    print("  [DRIVER] Yeni session başlatıldı.")
    return new_driver


# =====================================================================
# v3: PROFİL EKRAN GÖRÜNTÜSÜ + HEADER KIRPMA
# =====================================================================

def _get_header_bottom(driver, img_h: int) -> Tuple[int, str]:
    """
    Profil header'ının sayfa içindeki alt sınırını piksel olarak döner.
    Önce DOM seçicilerini dener; başarısız olursa HEADER_FALLBACK_HEIGHT kullanır.
    Returns: (bottom_px, kaynak_etiketi)
    """
    for sel in HEADER_CROP_SELECTORS:
        try:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            if not els:
                continue
            # Seçicinin tüm eşleşmeleri arasında en alttakini bul
            max_bottom = 0
            for el in els:
                rect = driver.execute_script(
                    "const r = arguments[0].getBoundingClientRect();"
                    "return {top: r.top, bottom: r.bottom};", el
                )
                if rect and rect["bottom"] > rect["top"]:
                    max_bottom = max(max_bottom, int(rect["bottom"]))
            if max_bottom > 0:
                scroll_y = int(driver.execute_script("return window.scrollY;") or 0)
                bottom   = min(img_h, max_bottom + scroll_y + HEADER_EXTRA_BOTTOM)
                return bottom, f"DOM:{sel[:30]}"
        except Exception:
            continue
    # Fallback
    return min(img_h, HEADER_FALLBACK_HEIGHT), "fallback"


def take_profile_screenshots(driver, uname: str) -> Tuple[str, str]:
    """
    1. Tam sayfa ekran görüntüsü alır → screenshots/full/
    2. Profil header bölgesini keser  → screenshots/cropped/

    Kırpma: tam genişlik (sol=0, sağ=ekran genişliği),
            yükseklik DOM'daki header elementinin gerçek alt sınırına kadar.
            DOM bulunamazsa HEADER_FALLBACK_HEIGHT px yükseklik kullanılır.

    Returns: (full_path_str, cropped_path_str)
    """
    stamp     = ts()
    fname     = f"profile_{safe_filename(uname)}_{stamp}"
    full_path = SHOT_FULL_DIR / f"{fname}.png"
    crop_path = SHOT_CROP_DIR / f"{fname}.png"

    # Sayfayı en üste getir — koordinatlar scroll'dan etkilenmesin
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.6)

    # ── 1. Tam sayfa ekran görüntüsü ──────────────────────────────
    png_bytes = driver.get_screenshot_as_png()
    full_img  = Image.open(io.BytesIO(png_bytes))
    full_img.save(str(full_path))
    img_w, img_h = full_img.size
    print(f"  [SS-FULL]  {full_path.name}  ({img_w}x{img_h}px)")

    # ── 2. Header alt sınırını bul, tam genişlikte kırp ───────────
    bottom, source = _get_header_bottom(driver, img_h)
    # Üst kırpma: sayfanın en tepesinden başla (top=0)
    crop_box = (0, 0, img_w, bottom)
    print(f"  [SS-CROP]  (0,0)→({img_w},{bottom})  [{source}]")

    cropped = full_img.crop(crop_box)
    cropped.save(str(crop_path))
    print(f"  [SS-CROP]  {crop_path.name}  ({img_w}x{bottom}px)")

    return str(full_path), str(crop_path)



# =====================================================================
# PROFİL KAZIMA
# =====================================================================

def _js_text(driver, js: str) -> Optional[str]:
    try:
        result = driver.execute_script(js)
        if result and str(result).strip():
            return str(result).strip()
    except Exception:
        pass
    return None

def scrape_profile(driver, username_or_url: str, retry: bool = True) -> Tuple[Dict[str, Any], webdriver.Chrome]:
    uname = normalize_username(username_or_url)
    url   = get_profile_url(username_or_url)

    ok, driver = smart_get(driver, url, expected_css=PROFILE_EXPECTED, context=f"profile_{uname}")
    if not ok:
        hp = save_debug_html(driver, f"profile_fail_{uname}")
        return _empty_profile(uname, url, "profile_nav_failed", hp), driver

    # ── Temel profil alanları ──────────────────────────────────────
    username     = text_or_none(driver, 'h1[data-e2e="user-title"]') or uname
    display_name = (
        text_or_none(driver, 'h2[data-e2e="user-subtitle"]')
        or text_or_none(driver, '[data-e2e="user-subtitle"]')
    )
    bio = (
        text_or_none(driver, 'h2[data-e2e="user-bio"]')
        or text_or_none(driver, '[data-e2e="user-bio"]')
        or _js_text(driver, """
            const el = document.querySelector('[data-e2e="user-bio"], .tiktok-1vll1nz-H2ShareDesc');
            return el ? el.innerText : null;
        """)
    )

    # ── Sayısal alanlar ───────────────────────────────────────────
    followers_txt = (
        text_or_none(driver, 'strong[data-e2e="followers-count"]')
        or text_or_none(driver, '[data-e2e="followers-count"]')
    )
    following_txt = (
        text_or_none(driver, 'strong[data-e2e="following-count"]')
        or text_or_none(driver, '[data-e2e="following-count"]')
    )
    likes_txt = (
        text_or_none(driver, 'strong[data-e2e="likes-count"]')
        or text_or_none(driver, '[data-e2e="likes-count"]')
    )
    website_url = (
        attr_or_none(driver, 'a[data-e2e="user-link"]', "href")
        or attr_or_none(driver, '[data-e2e="user-link"]', "href")
    )

    followers = parse_number(followers_txt)
    following = parse_number(following_txt)
    likes     = parse_number(likes_txt)

    # ── Followers güvenilirlik kontrolü ───────────────────────────
    followers_suspicious = False
    if followers is not None and followers < FOLLOWERS_SANITY_MIN:
        raw_src = driver.page_source
        big_num = re.search(
            r'(\d[\d,.]*[KMB]?)\s*(?:Takip|Follower)', raw_src, re.IGNORECASE
        )
        if big_num and parse_number(big_num.group(1)) \
                and parse_number(big_num.group(1)) > FOLLOWERS_SANITY_MIN:
            followers_suspicious = True
            print(f"  [UYARI] {uname}: followers={followers} şüpheli (sayfa: {big_num.group(1)})")
            if retry:
                print("  [RETRY] Profil yeniden çekiliyor...")
                time.sleep(3)
                return scrape_profile(driver, username_or_url, retry=False)
        elif followers < FOLLOWERS_SANITY_MIN:
            followers_suspicious = True

    # ── Son video tarihi / yayın sıklığı ─────────────────────────
    last_post_days_ago = None
    try:
        time_els = driver.find_elements(
            By.CSS_SELECTOR, '[data-e2e="video-create-time"], time'
        )
        for tel in time_els[:3]:
            raw_t = tel.text.strip() or tel.get_attribute("datetime")
            iso   = try_parse_posted_at(raw_t)
            days  = days_since(iso)
            if days is not None:
                last_post_days_ago = days
                break
    except Exception:
        pass

    # ── Görünen toplam video sayısı ───────────────────────────────
    post_count_visible = None
    try:
        cnt_el = driver.find_elements(By.CSS_SELECTOR,
            '[data-e2e="user-post-item-list"] [class*="DivItemContainer"], '
            '[data-e2e="user-post-item"]'
        )
        if cnt_el:
            post_count_visible = len(cnt_el)
    except Exception:
        pass

    # ── v3: Ekran görüntüsü al + header kırp ─────────────────────
    html_path = save_debug_html(driver, f"profile_{uname}")
    full_shot, crop_shot = take_profile_screenshots(driver, uname)

    return {
        "normalized_username"    : uname,
        "profile_url"            : url,
        "username"               : username,
        "display_name"           : display_name,
        "bio"                    : bio,
        "followers"              : followers,
        "following"              : following,
        "likes"                  : likes,
        "website_url"            : website_url,
        "followers_suspicious"   : followers_suspicious,
        "post_count_visible"     : post_count_visible,
        "last_post_days_ago"     : last_post_days_ago,
        "avg_video_likes_profile": None,
        "debug_html_path"        : html_path,
        "screenshot_full_path"   : full_shot,
        "screenshot_cropped_path": crop_shot,
        "error"                  : None,
    }, driver

def _empty_profile(uname, url, error, hp) -> Dict[str, Any]:
    return {
        "normalized_username"    : uname,
        "profile_url"            : url,
        "username"               : uname,
        "display_name"           : None,
        "bio"                    : None,
        "followers"              : None,
        "following"              : None,
        "likes"                  : None,
        "website_url"            : None,
        "followers_suspicious"   : None,
        "post_count_visible"     : None,
        "last_post_days_ago"     : None,
        "avg_video_likes_profile": None,
        "debug_html_path"        : hp,
        "screenshot_full_path"   : None,
        "screenshot_cropped_path": None,
        "error"                  : error,
    }


# =====================================================================
# VİDEO LİNKLERİ TOPLAMA
# =====================================================================

PINNED_HINTS = ["pinned", "sabitle", "sabitlendi", "sabit"]

def collect_video_links(driver, max_videos: int) -> List[Dict[str, Any]]:
    out : List[Dict[str, Any]] = []
    seen: set = set()

    def is_pinned_anchor(a_el) -> bool:
        try:
            node = a_el
            for _ in range(6):
                node = node.find_element(By.XPATH, "..")
                if any(h in (node.text or "").lower() for h in PINNED_HINTS):
                    return True
        except Exception:
            pass
        return False

    for step in range(PROFILE_SCROLL_STEPS):
        try:
            anchors = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/video/"]')
            for a in anchors:
                href = a.get_attribute("href") or ""
                if "/video/" not in href:
                    continue
                vurl = href.split("?")[0]
                if vurl in seen:
                    continue
                seen.add(vurl)
                out.append({
                    "video_url"            : vurl,
                    "is_pinned"            : is_pinned_anchor(a),
                    "video_rank_on_profile": len(out) + 1,
                })
                if len(out) >= max_videos:
                    return out
        except Exception:
            pass

        try:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        except Exception:
            pass
        time.sleep(2.0)

        if is_challenge(driver):
            wait_challenge_clears(driver, "collect_video_links")

    return out[:max_videos]


# =====================================================================
# VİDEO KAZIMA — v2: Kapsamlı Seçici Zinciri
# =====================================================================

VIEWS_SELECTORS = [
    'strong[data-e2e="play-count"]',
    '[data-e2e="play-count"]',
    'strong[data-e2e="video-play-count"]',
    '[data-e2e="video-views-count"]',
    '[data-e2e="browse-view-count"]',
    '[class*="video-count"]',
    '[class*="play-count"]',
    'strong[data-e2e="views-count"]',
]

CAPTION_SELECTORS = [
    '[data-e2e="browse-video-desc"]',
    'h1[data-e2e="video-desc"]',
    '[data-e2e="video-desc"]',
    '[class*="video-desc"]',
    '[class*="DivVideoInfoContainer"] span',
    '[class*="desc-text"]',
]

LIKES_SELECTORS = [
    'strong[data-e2e="like-count"]',
    '[data-e2e="like-count"]',
    '[data-e2e="browse-like-count"]',
    'strong[data-e2e="video-like-count"]',
]

COMMENTS_SELECTORS = [
    'strong[data-e2e="comment-count"]',
    '[data-e2e="comment-count"]',
    '[data-e2e="browse-comment-count"]',
]

SHARES_SELECTORS = [
    'strong[data-e2e="share-count"]',
    '[data-e2e="share-count"]',
    '[data-e2e="browse-share-count"]',
]

MUSIC_SELECTORS = [
    '[data-e2e="browse-music"]',
    '[data-e2e="video-music"]',
    'a[href*="/music/"]',
    '[class*="music-title"]',
]

POSTED_AT_SELECTORS = [
    '[data-e2e="browse-post-time"]',
    '[data-e2e="video-create-time"]',
    'span[data-e2e="video-creation-time"]',
    '[class*="create-time"]',
    '[class*="video-time"]',
    'time',
]

COMMENTS_DISABLED_HINTS = [
    "comments are turned off", "comments have been turned off",
    "yorumlar kapalı", "yorumlar devre dışı", "yorum kapalı",
]


def _try_selectors(driver, selectors: List[str]) -> Tuple[Optional[str], Optional[str]]:
    for css in selectors:
        val = text_or_none(driver, css)
        if val:
            return val, css
    return None, None


def _js_views(driver) -> Tuple[Optional[str], str]:
    js = """
    const e2e = document.querySelector('[data-e2e*="play"], [data-e2e*="view"], [data-e2e*="count"]');
    if (e2e && /^[\\d\\.]+[KMBkmb]?$/.test(e2e.innerText.trim())) return e2e.innerText.trim();

    const candidates = Array.from(
        document.querySelectorAll('strong, span[class*="count"], span[class*="number"]')
    );
    for (const el of candidates) {
        const t = el.innerText.trim();
        if (/^[\\d\\.]+[KMBkmb]?$/.test(t) && el.innerText.length <= 8) {
            const pText = (el.parentElement?.innerText || '').toLowerCase();
            if (pText.includes('view') || pText.includes('play') ||
                pText.includes('izlenme') || pText.includes('görüntülenme')) {
                return t;
            }
        }
    }

    const scripts = document.querySelectorAll('script[type="application/ld+json"]');
    for (const s of scripts) {
        try {
            const d = JSON.parse(s.innerText);
            if (d.interactionStatistic) {
                for (const stat of d.interactionStatistic) {
                    if (stat['@type'] === 'WatchAction' || stat.name === 'Watch') {
                        return String(stat.userInteractionCount);
                    }
                }
            }
        } catch(e) {}
    }
    return null;
    """
    try:
        result = driver.execute_script(js)
        if result and str(result).strip():
            return str(result).strip(), "js_fallback"
    except Exception:
        pass
    return None, "not_found"


def _js_caption(driver) -> Tuple[Optional[str], str]:
    js = """
    const e = document.querySelector('[data-e2e*="desc"], [data-e2e*="caption"]');
    if (e && e.innerText.trim().length > 3) return e.innerText.trim();

    const h1s = document.querySelectorAll('h1');
    for (const h of h1s) {
        if (h.innerText.trim().length > 5 && h.innerText.length < 1000) {
            return h.innerText.trim();
        }
    }

    const divs = document.querySelectorAll('div[class*="desc"], div[class*="caption"], span[class*="desc"]');
    for (const d of divs) {
        const t = d.innerText.trim();
        if (t.length > 5 && t.length < 2000) return t;
    }
    return null;
    """
    try:
        result = driver.execute_script(js)
        if result and str(result).strip():
            return str(result).strip(), "js_fallback"
    except Exception:
        pass
    return None, "not_found"


def get_video_duration_sec(driver) -> Optional[float]:
    js = """
    const v = document.querySelector('video');
    if (!v) return null;
    const d = v.duration;
    return (d && isFinite(d)) ? d : null;
    """
    try:
        d = driver.execute_script(js)
        return float(d) if d is not None else None
    except Exception:
        return None


def detect_comments_enabled(driver) -> Tuple[Optional[bool], Optional[str]]:
    try:
        src = (driver.page_source or "").lower()
        for h in COMMENTS_DISABLED_HINTS:
            if h in src:
                return False, h
    except Exception:
        pass
    val, _ = _try_selectors(driver, COMMENTS_SELECTORS)
    if val is not None:
        return True, None
    return None, None


def find_posted_at(driver) -> Optional[str]:
    for css in POSTED_AT_SELECTORS:
        t = text_or_none(driver, css)
        if t:
            if css == "time":
                dt = attr_or_none(driver, "time", "datetime")
                return dt or t
            return t
    try:
        src = driver.page_source
        for pat in [
            r"(\d+\s*(?:gün|saat|dakika)\s*önce)",
            r"(\d+\s*(?:days?|hours?|minutes?)\s*ago)",
            r'"createTime"\s*:\s*"?(\d{10})"?',
        ]:
            m = re.search(pat, src, re.IGNORECASE)
            if m:
                val = m.group(1)
                if re.match(r"^\d{10}$", val):
                    return datetime.fromtimestamp(int(val)).isoformat()
                return val
    except Exception:
        pass
    return None


def scrape_video(
    driver,
    video_url       : str,
    profile_username: str,
    is_pinned       : bool,
    rank_on_profile : Optional[int],
) -> Tuple[Dict[str, Any], webdriver.Chrome]:

    ok, driver = smart_get(driver, video_url, expected_css=VIDEO_EXPECTED,
                            context=f"video_{profile_username}")
    if not ok:
        hp = save_debug_html(driver, f"video_fail_{profile_username}")
        return {
            **{f: None for f in VIDEO_FIELDS},
            "profile_username"     : profile_username,
            "video_url"            : video_url,
            "video_rank_on_profile": rank_on_profile,
            "is_pinned"            : is_pinned,
            "error"                : "video_nav_failed",
            "debug_html_path"      : hp,
        }, driver

    # ── Caption ───────────────────────────────────────────────────
    caption, caption_source = _try_selectors(driver, CAPTION_SELECTORS)
    if not caption:
        caption, caption_source = _js_caption(driver)

    hashtags_list = extract_hashtags(caption)
    hashtag_count = len(hashtags_list)

    # ── Etkileşim metrikleri ──────────────────────────────────────
    likes_txt,    _ = _try_selectors(driver, LIKES_SELECTORS)
    comments_txt, _ = _try_selectors(driver, COMMENTS_SELECTORS)
    shares_txt,   _ = _try_selectors(driver, SHARES_SELECTORS)

    # ── views ─────────────────────────────────────────────────────
    views_txt, views_source = _try_selectors(driver, VIEWS_SELECTORS)
    if not views_txt:
        views_txt, views_source = _js_views(driver)

    # ── Müzik ─────────────────────────────────────────────────────
    music, _ = _try_selectors(driver, MUSIC_SELECTORS)

    # ── Tarih ─────────────────────────────────────────────────────
    posted_at_raw = find_posted_at(driver)
    posted_at_iso = try_parse_posted_at(posted_at_raw)

    # ── Video süresi ──────────────────────────────────────────────
    video_duration_sec = get_video_duration_sec(driver)

    # ── Yorum durumu ──────────────────────────────────────────────
    comments_enabled, comments_disabled_reason = detect_comments_enabled(driver)

    # ── Sayıları parse et ─────────────────────────────────────────
    views     = parse_number(views_txt)
    vlikes    = parse_number(likes_txt)
    vcomments = parse_number(comments_txt)
    vshares   = parse_number(shares_txt)

    # ── Oranlar ───────────────────────────────────────────────────
    like_rate       = (vlikes / views) if (views and vlikes) else None
    engagement_rate = (
        ((vlikes or 0) + (vcomments or 0) + (vshares or 0)) / views
        if views else None
    )

    # ── Sponsorlu içerik tespiti ──────────────────────────────────
    is_sponsored, sponsored_tag = detect_sponsored(caption)

    # v3: video sayfalarında sadece HTML debug kaydedilir; ss alınmaz
    hp = save_debug_html(driver, f"video_{profile_username}")

    return {
        "profile_username"         : profile_username,
        "video_url"                : video_url,
        "video_rank_on_profile"    : rank_on_profile,
        "is_pinned"                : bool(is_pinned),
        "caption"                  : caption,
        "hashtags"                 : ",".join(hashtags_list) if hashtags_list else None,
        "hashtag_count"            : hashtag_count,
        "music_text"               : music,
        "posted_at_raw"            : posted_at_raw,
        "posted_at_iso"            : posted_at_iso,
        "video_duration_sec"       : video_duration_sec,
        "views"                    : views,
        "video_likes"              : vlikes,
        "comments"                 : vcomments,
        "shares"                   : vshares,
        "like_rate"                : like_rate,
        "engagement_rate"          : engagement_rate,
        "comments_enabled"         : comments_enabled,
        "comments_disabled_reason" : comments_disabled_reason,
        "is_sponsored"             : is_sponsored,
        "sponsored_tag"            : sponsored_tag,
        "caption_source"           : caption_source,
        "views_source"             : views_source,
        "debug_html_path"          : hp,
        "error"                    : None,
    }, driver


# =====================================================================
# KULLANICI LİSTESİ
# =====================================================================

def load_users() -> List[str]:
    if not TXT_FILE.exists():
        print(f"[UYARI] {TXT_FILE} bulunamadı. Demo kullanıcılarla devam ediliyor.")
        return ["tiktok", "khaby.lame", "charlidamelio"]
    users = []
    with TXT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                users.append(s)
    return users


# =====================================================================
# EXCEL ÜRETİMİ
# =====================================================================

def finalize_excel():
    print("\n[EXCEL] Profil ve video verileri Excel'e aktarılıyor...")
    dfp = dfv = None

    if PROFILES_CSV.exists():
        try:
            dfp = pd.read_csv(PROFILES_CSV, engine="python", on_bad_lines="skip")
        except Exception as e:
            print(f"[HATA] profiles.csv okunamadı: {e}")

    if VIDEOS_CSV.exists():
        try:
            dfv = pd.read_csv(VIDEOS_CSV, engine="python", on_bad_lines="skip")
        except Exception as e:
            print(f"[HATA] videos.csv okunamadı: {e}")

    if dfp is None or dfp.empty:
        print("[UYARI] Profil verisi yok, Excel üretimi atlandı.")
        return

    for col in ["normalized_username", "username"]:
        if col not in dfp.columns:
            dfp[col] = dfp.get("username", dfp.get("normalized_username", "unknown"))

    for col in ["followers", "following", "likes"]:
        if col in dfp.columns:
            dfp[col] = pd.to_numeric(dfp[col], errors="coerce").fillna(0)

    dfp["like_per_follower"] = dfp.apply(
        lambda r: r["likes"] / r["followers"]
        if r.get("followers", 0) > 0 and pd.notna(r.get("likes")) else 0,
        axis=1
    )

    if dfv is not None and not dfv.empty:
        dfv["video_likes_n"]     = pd.to_numeric(dfv.get("video_likes", 0), errors="coerce").fillna(0)
        dfv["views_n"]           = pd.to_numeric(dfv.get("views", 0),       errors="coerce").fillna(0)
        dfv["comments_n"]        = pd.to_numeric(dfv.get("comments", 0),    errors="coerce").fillna(0)
        dfv["shares_n"]          = pd.to_numeric(dfv.get("shares", 0),      errors="coerce").fillna(0)
        dfv["total_interaction"] = dfv["video_likes_n"] + dfv["comments_n"] + dfv["shares_n"]

        agg = dfv.groupby("profile_username").agg(
            avg_video_likes       = ("video_likes_n",    "mean"),
            avg_video_views       = ("views_n",          "mean"),
            avg_total_interaction = ("total_interaction","mean"),
            scraped_video_count   = ("video_url",        "count"),
        ).reset_index()

        dfp = dfp.merge(
            agg, left_on="normalized_username",
            right_on="profile_username", how="left"
        ).drop(columns=["profile_username"], errors="ignore")

        dfv["eng_rate"] = dfv.apply(
            lambda r: r["total_interaction"] / r["views_n"]
            if r["views_n"] > 0 else None, axis=1
        )
        eng = dfv.groupby("profile_username")["eng_rate"].mean().reset_index()
        eng.columns = ["normalized_username", "avg_video_engagement"]
        dfp = dfp.merge(eng, on="normalized_username", how="left")

    for col in ["avg_video_engagement", "avg_video_likes", "avg_total_interaction"]:
        dfp[col] = dfp.get(col, 0).fillna(0)

    def norm(s):
        s  = pd.to_numeric(s, errors="coerce").fillna(0)
        mn, mx = s.min(), s.max()
        return 100 * (s - mn) / (mx - mn) if mx > mn else pd.Series([50]*len(s), index=s.index)

    dfp["followers_log"]    = np.log1p(dfp["followers"])
    dfp["influencer_score"] = (
        0.40 * norm(dfp["avg_total_interaction"].fillna(dfp["avg_video_likes"])) +
        0.35 * norm(dfp["followers_log"]) +
        0.25 * norm(dfp["like_per_follower"])
    ).round(2)

    dfp.sort_values("influencer_score", ascending=False, inplace=True)

    dfp.to_excel(DATA_DIR / "tiktok_profiles.xlsx", index=False)
    if dfv is not None:
        dfv.to_excel(DATA_DIR / "tiktok_videos.xlsx", index=False)

    print("✅ tiktok_profiles.xlsx ve tiktok_videos.xlsx oluşturuldu.")


# =====================================================================
# KATEGORİLENDİRME MODÜLÜ
# =====================================================================

OUT_PROFILES_CAT = DATA_DIR / "tiktok_profiles_categorized.xlsx"
OUT_VIDEOS_CAT   = DATA_DIR / "tiktok_videos_categorized.xlsx"

MAX_VIDEOS_FOR_CAT = 10

W_HASHTAG = 3.0
W_CAPTION = 1.5
W_BIO     = 2.0
W_MUSIC   = 0.5

STOP_HASHTAGS = {
    "fyp","foryou","foryoupage","viral","trend","trending",
    "tiktok","keşfet","kesfet","explore","fy","parati",
}

CATEGORIES: Dict[str, Dict[str, List[str]]] = {
    "Beauty & Personal Care": {"kw": [
        "makeup","skincare","beauty","cosmetics","glow","foundation","lipstick",
        "hair","hairstyle","nail","perfume","routine","moisturizer","serum",
        "makyaj","cilt","ciltbakım","ciltbakimi","kozmetik","saç","sac",
        "bakım","bakim","parfüm","parfum","nemlendirici","ruj","fondöten",
    ]},
    "Fashion & Style": {"kw": [
        "outfit","style","fashion","haul","trend","lookbook","wardrobe","ootd",
        "kombin","moda","stil","giyim","alışveriş","alisveris","dolap","tarz",
        "kıyafet","kiyafet","giysi",
    ]},
    "Fitness & Health": {"kw": [
        "workout","gym","fitness","cardio","protein","strength","training",
        "diet","health","exercise","muscle","yoga","pilates",
        "spor","antrenman","kas","kilo","diyet","sağlık","saglik","egzersiz",
    ]},
    "Food & Cooking": {"kw": [
        "recipe","cooking","food","chef","kitchen","mukbang","baking","dessert",
        "restaurant","yemek","mutfak","aşçı","asci","pasta","tatlı","tatli",
        "lezzet","tarif","pişirmek","pisirmek","restoran",
    ]},
    "Comedy & Entertainment": {"kw": [
        "funny","comedy","prank","joke","skit","meme","lol","humor","hilarious",
        "komedi","şaka","saka","eğlence","eglence","skeç","skec","mizah",
        "gülmek","gulmek","espri",
    ]},
    "Gaming": {"kw": [
        "gaming","gameplay","stream","streamer","esports","gamer","pc","console",
        "fortnite","valorant","minecraft","pubg","cs2","lol","leagueoflegends",
        "oyun","yayın","yayin","oyuncu","turnuva",
    ]},
    "Technology & Digital": {"kw": [
        "tech","technology","software","ai","gadget","review","iphone","android",
        "app","coding","python","data","programming","developer","startup",
        "teknoloji","yapay zeka","uygulama","kod","yazılım","yazilim","inceleme",
    ]},
    "Education & Informative": {"kw": [
        "tutorial","tips","howto","learn","education","explained","guide","lesson",
        "study","knowledge","ders","eğitim","egitim","anlatım","anlatim",
        "ipucu","nasıl","nasil","rehber","öğren","ogren","bilgi",
    ]},
    "Travel & Lifestyle": {"kw": [
        "travel","trip","vlog","lifestyle","routine","daily","morning","adventure",
        "vacation","holiday","gezi","seyahat","günlük","gunluk","rutin","hayat",
        "yaşam","yasam","tatil","keşif","kesif",
    ]},
    "Music & Performance": {"kw": [
        "music","dance","singing","performance","cover","song","choreo","concert",
        "artist","müzik","muzik","dans","şarkı","sarki","performans","konser",
        "sanatçı","sanatci","enstrüman","enstruman",
    ]},
    "Sports & MMA": {"kw": [
        "mma","ufc","boxing","fight","fighter","martial","wrestling","bjj",
        "kickboxing","muaythai","dövüş","dovus","güreş","gures","boks",
        "futbol","basketball","soccer","nba","football",
    ]},
}

def _norm(x) -> str:
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return ""
    return str(x).replace("\n", " ").replace("\r", " ").lower().strip()

def _split_tags(field: str) -> List[str]:
    s = _norm(field)
    if not s:
        return []
    parts = [p.strip().lstrip("#") for p in s.split(",") if p.strip()]
    return [p for p in parts if p and p not in STOP_HASHTAGS]

def _hit(text: str, keywords: List[str]) -> int:
    t = _norm(text)
    if not t:
        return 0
    count = 0
    for kw in keywords:
        k = kw.lower().strip()
        if not k:
            continue
        if " " in k:
            count += 1 if k in t else 0
        else:
            count += 1 if re.search(rf"\b{re.escape(k)}\b", t) else 0
    return count

def _score(caption, hashtags, bio, music) -> Dict[str, float]:
    scores = {cat: 0.0 for cat in CATEGORIES}
    ht = " ".join(f"#{h}" for h in hashtags)
    for cat, spec in CATEGORIES.items():
        kw = spec["kw"]
        s  = 0.0
        s += W_CAPTION * _hit(caption, kw)
        s += W_BIO     * _hit(bio,     kw)
        s += W_MUSIC   * _hit(music,   kw)
        s += W_HASHTAG * _hit(ht,      kw)
        scores[cat] = s
    return scores

def _top2(scores: Dict[str, float]) -> Tuple[str, Optional[str], float, float]:
    items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    p, s1 = items[0]
    sec   = items[1][0] if len(items) > 1 else None
    total = sum(v for _, v in items)
    conf  = (s1 / total) if total > 0 else 0.0
    return p, sec, float(s1), float(conf)


def categorize_and_export():
    pp = DATA_DIR / "tiktok_profiles.xlsx"
    vp = DATA_DIR / "tiktok_videos.xlsx"

    if not pp.exists() or not vp.exists():
        print("[UYARI] Kategorilendirme atlandı: Excel dosyaları bulunamadı.")
        return

    dfp = pd.read_excel(pp)
    dfv = pd.read_excel(vp)

    if dfp.empty or dfv.empty:
        print("[UYARI] Kategorilendirme atlandı: boş veri.")
        return

    # ── Video seviyesi kategorilendirme ──
    vp_list, vs_list, vsc_list, vc_list = [], [], [], []
    for _, row in dfv.iterrows():
        tags   = _split_tags(row.get("hashtags"))
        scores = _score(
            caption  = row.get("caption", ""),
            hashtags = tags,
            bio      = "",
            music    = row.get("music_text", ""),
        )
        p, s, sc, conf = _top2(scores)
        vp_list.append(p);  vs_list.append(s)
        vsc_list.append(sc); vc_list.append(conf)

    dfv["category_primary_video"]    = vp_list
    dfv["category_secondary_video"]  = vs_list
    dfv["category_score_video"]      = vsc_list
    dfv["category_confidence_video"] = vc_list

    # ── Profil seviyesi kategorilendirme ──
    prof_key = "normalized_username" if "normalized_username" in dfp.columns else "username"
    vid_key  = "profile_username"

    if vid_key not in dfv.columns:
        print("[UYARI] Kategorilendirme atlandı: video tablosunda profile_username yok.")
        return

    grp = dfv.groupby(vid_key, dropna=False)

    pp_list, ps_list, psc_list, pc_list = [], [], [], []
    for _, prow in dfp.iterrows():
        uname = prow.get(prof_key)
        bio   = prow.get("bio", "") or ""

        vids = grp.get_group(uname).head(MAX_VIDEOS_FOR_CAT) \
               if uname in grp.groups else dfv.iloc[0:0]

        agg = {cat: 0.0 for cat in CATEGORIES}

        for cat, v in _score("", [], bio, "").items():
            agg[cat] += v

        for _, vrow in vids.iterrows():
            tags = _split_tags(vrow.get("hashtags"))
            for cat, v in _score(
                vrow.get("caption",""), tags, "", vrow.get("music_text","")
            ).items():
                agg[cat] += v

        p, s, sc, conf = _top2(agg)
        pp_list.append(p);  ps_list.append(s)
        psc_list.append(sc); pc_list.append(conf)

    dfp["category_primary"]   = pp_list
    dfp["category_secondary"] = ps_list
    dfp["category_score"]     = psc_list
    dfp["category_confidence"]= pc_list

    dfp["category_primary_final"] = dfp.apply(
        lambda r: "Mixed/Unclear"
        if r.get("category_confidence", 0) < CATEGORY_CONFIDENCE_THRESHOLD
        else r.get("category_primary"),
        axis=1
    )

    dfp.to_excel(OUT_PROFILES_CAT, index=False)
    dfv.to_excel(OUT_VIDEOS_CAT,   index=False)

    cat_dist = dfp["category_primary_final"].value_counts()
    print("\n[KATEGORİ] Dağılım:")
    for cat, cnt in cat_dist.items():
        print(f"  {cat:30s}: {cnt}")

    print(f"\n✅ {OUT_PROFILES_CAT.name}")
    print(f"✅ {OUT_VIDEOS_CAT.name}")


# =====================================================================
# ANA DÖNGÜ
# =====================================================================

def main():
    users = load_users()
    state = load_state()

    done_users  = set(state.get("done_users",  []))
    done_videos = set(state.get("done_videos", []))

    remaining = [u for u in users if normalize_username(u) not in done_users]

    print("=" * 60)
    print("  TikTok Scraper v3.1")
    print("=" * 60)
    print(f"  Toplam kullanıcı      : {len(users)}")
    print(f"  Tamamlanan            : {len(done_users)}")
    print(f"  Kalan                 : {len(remaining)}")
    print(f"  Profil başına video   : {MAX_VIDEOS_PER_PROFILE}")
    print(f"  Çıktı klasörü         : {DATA_DIR.resolve()}")
    print(f"  Tam SS klasörü        : {SHOT_FULL_DIR.resolve()}")
    print(f"  Kırpılmış SS klasörü  : {SHOT_CROP_DIR.resolve()}")
    print("=" * 60)
    print()
    print("  ⚠️  UYKU MODU UYARISI: Bilgisayarın uyku moduna geçmesi")
    print("     Chrome session'ını öldürür. Çalıştırmadan önce:")
    print("     macOS  → Terminal: caffeinate -i python tiktok_scrapper_v3.py")
    print("     Windows→ Güç ayarları > Uyku: Asla")
    print("=" * 60)

    driver = create_driver()

    try:
        _, driver = smart_get(driver, "https://www.tiktok.com/", ["body"], "home_boot")
        if is_challenge(driver):
            wait_challenge_clears(driver, "home_boot")

        for idx, u in enumerate(users, start=1):
            uname = normalize_username(u)
            if uname in done_users:
                continue

            print(f"\n[{idx}/{len(users)}] {uname}")

            # ── Driver sağlık kontrolü — her profil öncesi ──
            if not is_driver_alive(driver):
                driver = restart_driver(driver)
                # Ana sayfaya dön, yeni session'ı ısıt
                _, driver = smart_get(driver, "https://www.tiktok.com/", ["body"], "restart_boot")

            # ── Profil kazı ──
            try:
                prof, driver = scrape_profile(driver, u)
            except Exception as e:
                print(f"  [HATA] scrape_profile beklenmedik hata: {e}")
                prof = _empty_profile(uname, get_profile_url(u), str(e), "")
                if not is_driver_alive(driver):
                    driver = restart_driver(driver)

            append_csv_fixed(PROFILES_CSV, PROFILE_FIELDS, prof)

            if prof.get("error"):
                print(f"  [HATA] Profil atlandı: {prof['error']}")
                done_users.add(uname)
                state["done_users"] = sorted(done_users)
                save_state(state)
                jitter_sleep(SLEEP_BETWEEN_PROFILES)
                continue

            print(f"  followers={prof.get('followers')}  "
                  f"suspicious={prof.get('followers_suspicious')}  "
                  f"son_gönderi={prof.get('last_post_days_ago')} gün önce")

            # ── Video linklerini topla ──
            links = collect_video_links(driver, MAX_VIDEOS_PER_PROFILE)
            print(f"  Video linki bulundu: {len(links)}")

            # ── Her videoyu kazı ──
            for item in links:
                vurl   = item["video_url"]
                pinned = item.get("is_pinned", False)
                rank   = item.get("video_rank_on_profile")
                key    = f"{uname}|{vurl}"

                if key in done_videos:
                    continue

                try:
                    vrow, driver = scrape_video(driver, vurl, uname, pinned, rank)
                except Exception as e:
                    print(f"    [HATA] scrape_video beklenmedik hata: {e}")
                    vrow = {f: None for f in VIDEO_FIELDS}
                    vrow.update({"profile_username": uname, "video_url": vurl,
                                 "video_rank_on_profile": rank, "is_pinned": pinned,
                                 "error": str(e)})
                    if not is_driver_alive(driver):
                        driver = restart_driver(driver)

                append_csv_fixed(VIDEOS_CSV, VIDEO_FIELDS, vrow)

                vsrc = vrow.get("views_source", "?")
                vval = vrow.get("views")
                print(f"    [{rank}] views={vval} ({vsrc})  "
                      f"likes={vrow.get('video_likes')}  "
                      f"sponsored={vrow.get('is_sponsored')}")

                done_videos.add(key)
                state["done_videos"] = sorted(done_videos)
                save_state(state)
                jitter_sleep(SLEEP_BETWEEN_VIDEOS)

            done_users.add(uname)
            state["done_users"] = sorted(done_users)
            save_state(state)
            jitter_sleep(SLEEP_BETWEEN_PROFILES)

    finally:
        try:
            driver.quit()
        except Exception:
            pass
        print("\n[BİTİŞ] Driver kapatıldı.")

    # ── Post-processing ──
    finalize_excel()
    categorize_and_export()

    print("\n" + "=" * 60)
    print("  TAMAMLANDI")
    print("=" * 60)
    print(f"  profiles.csv            : {PROFILES_CSV}")
    print(f"  videos.csv              : {VIDEOS_CSV}")
    print(f"  Excel (profil)          : {DATA_DIR / 'tiktok_profiles.xlsx'}")
    print(f"  Excel (video)           : {DATA_DIR / 'tiktok_videos.xlsx'}")
    print(f"  Categorized profil      : {OUT_PROFILES_CAT}")
    print(f"  Categorized video       : {OUT_VIDEOS_CAT}")
    print(f"  Debug HTML              : {RAW_HTML_DIR}")
    print(f"  SS (tam)                : {SHOT_FULL_DIR}")
    print(f"  SS (kırpılmış header)   : {SHOT_CROP_DIR}")
    print(f"  Checkpoint              : {STATE_FILE}")


if __name__ == "__main__":
    main()