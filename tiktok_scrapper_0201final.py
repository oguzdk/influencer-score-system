# -*- coding: utf-8 -*-
"""
TikTok Scraper — STABLE + CSV SAFE + EXTRA POST FIELDS + CATEGORIZATION (Selenium)
---------------------------------------------------------------------------------
- Login gerektirmez (login yaparsan daha stabil olabilir ama şart değil)
- Puzzle/verify gelirse DURUR ve bekler; çözülünce DEVAM eder
- Expected element geldi mi? mantığı
- Checkpoint + incremental CSV (CSV QUOTE_ALL -> bozulmaz)
- En sonda Excel üretir (read_csv: engine=python + on_bad_lines=skip)
- Son adım: Influencer kategorilendirme (10 kategori) ve categorized Excel üretimi

Çıktılar:
- data_tiktok/profiles.csv
- data_tiktok/videos.csv
- data_tiktok/tiktok_profiles.xlsx
- data_tiktok/tiktok_videos.xlsx
- data_tiktok/tiktok_profiles_categorized.xlsx
- data_tiktok/tiktok_videos_categorized.xlsx
- data_tiktok/raw_html/...
- data_tiktok/screenshots/...
- data_tiktok/run_state.json
"""
import numpy as np
import re
import json
import time
import random
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager


# =================== CONFIG ===================

DATA_DIR = Path("data_tiktok")
RAW_HTML_DIR = DATA_DIR / "raw_html"
SHOT_DIR = DATA_DIR / "screenshots"
STATE_FILE = DATA_DIR / "run_state.json"

PROFILES_CSV = DATA_DIR / "profiles.csv"
VIDEOS_CSV = DATA_DIR / "videos.csv"

TXT_FILE = Path("tiktok_kullanicilar.txt")

MAX_VIDEOS_PER_PROFILE = 10
PROFILE_SCROLL_STEPS = 6

SLEEP_BETWEEN_PROFILES = (4.0, 7.0)   # min/max
SLEEP_BETWEEN_VIDEOS = (2.5, 5.0)

HEADLESS = False
CHROME_PROFILE_DIR = Path("chrome_profile").resolve()

PAGE_WAIT_SEC = 20
CHALLENGE_WAIT_SEC = 20 * 60
NAV_RETRIES = 2

DATA_DIR.mkdir(exist_ok=True)
RAW_HTML_DIR.mkdir(exist_ok=True)
SHOT_DIR.mkdir(exist_ok=True)
CATEGORY_CONFIDENCE_THRESHOLD = 25  # ampirik eşik değer

# =================== CSV HEADERS (fixed) ===================

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
    "debug_html_path",
    "debug_screenshot_path",
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

    "debug_html_path",
    "debug_screenshot_path",
    "error",
]


# =================== HELPERS ===================

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
        m = re.search(r"@([^/?]+)", s)
        if m:
            return m.group(1)
    return s.lstrip("@")

def get_profile_url(username_or_url: str) -> str:
    raw = username_or_url.strip()
    if "tiktok.com" in raw:
        return raw
    u = normalize_username(username_or_url)
    return f"https://www.tiktok.com/@{u}"

def parse_number(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    t = text.strip().upper().replace(",", "")
    if not t:
        return None
    mult = 1
    if t.endswith("K"):
        mult = 1_000
        t = t[:-1]
    elif t.endswith("M"):
        mult = 1_000_000
        t = t[:-1]
    elif t.endswith("B"):
        mult = 1_000_000_000
        t = t[:-1]
    try:
        return int(float(t) * mult)
    except ValueError:
        return None

def save_debug(driver, tag: str):
    html_path = RAW_HTML_DIR / f"{safe_filename(tag)}_{ts()}.html"
    shot_path = SHOT_DIR / f"{safe_filename(tag)}_{ts()}.png"
    try:
        html_path.write_text(driver.page_source, encoding="utf-8")
    except Exception:
        pass
    try:
        driver.save_screenshot(str(shot_path))
    except Exception:
        pass
    return str(html_path), str(shot_path)

def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"done_users": [], "done_videos": []}

def save_state(state: Dict[str, Any]):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def append_csv_fixed(path: Path, fields: List[str], row: Dict[str, Any]):
    """
    Sabit kolon yapısı ile CSV append.
    CSV bozulmasını engeller:
    - QUOTE_ALL: virgül/newline içeren metinleri güvenle yazar
    - extrasaction=ignore: row ekstra key içerirse problem olmaz
    """
    import csv
    is_new = not path.exists()
    out = {k: row.get(k, None) for k in fields}
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fields,
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
                els = driver.find_elements(By.CSS_SELECTOR, css)
                if els:
                    return css
            except Exception:
                pass
        time.sleep(0.5)
    return None

def text_or_none(driver, css: str) -> Optional[str]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, css)
        t = el.text.strip()
        return t if t else None
    except Exception:
        return None

def attr_or_none(driver, css: str, attr: str) -> Optional[str]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, css)
        v = el.get_attribute(attr)
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
    s = raw.strip()

    m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", s)
    if m:
        try:
            dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            return dt.isoformat()
        except Exception:
            pass

    now = datetime.now()

    m = re.search(r"\b(\d+)\s*(day|days|d)\b", s, re.IGNORECASE)
    if m:
        return (now - timedelta(days=int(m.group(1)))).isoformat()

    m = re.search(r"\b(\d+)\s*(hour|hours|h)\b", s, re.IGNORECASE)
    if m:
        return (now - timedelta(hours=int(m.group(1)))).isoformat()

    m = re.search(r"\b(\d+)\s*(minute|minutes|min)\b", s, re.IGNORECASE)
    if m:
        return (now - timedelta(minutes=int(m.group(1)))).isoformat()

    m = re.search(r"\b(\d+)\s*gün\s*önce\b", s, re.IGNORECASE)
    if m:
        return (now - timedelta(days=int(m.group(1)))).isoformat()

    m = re.search(r"\b(\d+)\s*saat\s*önce\b", s, re.IGNORECASE)
    if m:
        return (now - timedelta(hours=int(m.group(1)))).isoformat()

    m = re.search(r"\b(\d+)\s*dakika\s*önce\b", s, re.IGNORECASE)
    if m:
        return (now - timedelta(minutes=int(m.group(1)))).isoformat()

    return None


# =================== CHALLENGE DETECTION ===================

CHALLENGE_HINT_SELECTORS = [
    'iframe[src*="captcha"]',
    'iframe[title*="captcha"]',
    '[id*="captcha"]',
    '[class*="captcha"]',
    '[class*="verify"]',
    '[class*="verification"]',
]

PROFILE_EXPECTED = [
    'h1[data-e2e="user-title"]',
    'strong[data-e2e="followers-count"]',
]

VIDEO_EXPECTED = [
    '[data-e2e="browse-video-desc"]',
    'h1[data-e2e="video-desc"]',
    'strong[data-e2e="like-count"]',
    'strong[data-e2e="comment-count"]',
    'a[href*="/music/"]',
]

def is_challenge_like(driver) -> bool:
    try:
        hit = wait_any(driver, CHALLENGE_HINT_SELECTORS, timeout=1)
        return hit is not None
    except Exception:
        return False

def wait_challenge_clears(driver, context: str):
    print(f"\n[PUZZLE] Challenge algılandı ({context}). Tarayıcıda çöz, bitince sayfa normale dönecek.")
    save_debug(driver, f"challenge_{context}")
    end = time.time() + CHALLENGE_WAIT_SEC
    while time.time() < end:
        time.sleep(1.0)
        if not is_challenge_like(driver):
            return
    print("[PUZZLE] Çok uzun sürdü. Devam için ENTER (çözdüysen) / çıkmak için Ctrl+C.")
    input(">> ")


# =================== SMART NAVIGATION ===================

def smart_get(driver, url: str, expected_css: List[str], context: str) -> bool:
    for attempt in range(1, NAV_RETRIES + 1):
        driver.get(url)
        time.sleep(1.5)

        hit = wait_any(driver, expected_css, timeout=PAGE_WAIT_SEC)
        if hit:
            return True

        if is_challenge_like(driver):
            wait_challenge_clears(driver, context=context)
            hit2 = wait_any(driver, expected_css, timeout=PAGE_WAIT_SEC)
            if hit2:
                return True

        save_debug(driver, f"nav_fail_{context}_attempt{attempt}")
        time.sleep(2)

    return False


# =================== DRIVER ===================

def create_driver() -> webdriver.Chrome:
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--start-maximized")
    opts.add_argument(f"--user-data-dir={str(CHROME_PROFILE_DIR)}")
    opts.add_argument("--profile-directory=Default")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


# =================== SCRAPE PROFILE ===================

def scrape_profile(driver, username_or_url: str) -> Dict[str, Any]:
    uname = normalize_username(username_or_url)
    url = get_profile_url(username_or_url)

    ok = smart_get(driver, url, expected_css=PROFILE_EXPECTED, context=f"profile_{uname}")
    if not ok:
        html_path, shot_path = save_debug(driver, f"profile_fail_{uname}")
        return {
            "normalized_username": uname,
            "profile_url": url,
            "username": uname,
            "display_name": None,
            "bio": None,
            "followers": None,
            "following": None,
            "likes": None,
            "website_url": None,
            "error": "profile_nav_failed",
            "debug_html_path": html_path,
            "debug_screenshot_path": shot_path,
        }

    username = text_or_none(driver, 'h1[data-e2e="user-title"]') or uname
    display_name = text_or_none(driver, 'h2[data-e2e="user-subtitle"]')
    bio = text_or_none(driver, 'h2[data-e2e="user-bio"]')

    followers_txt = text_or_none(driver, 'strong[data-e2e="followers-count"]')
    following_txt = text_or_none(driver, 'strong[data-e2e="following-count"]')
    likes_txt = text_or_none(driver, 'strong[data-e2e="likes-count"]')

    website_url = attr_or_none(driver, 'a[data-e2e="user-link"]', "href")

    html_path, shot_path = save_debug(driver, f"profile_{uname}")

    return {
        "normalized_username": uname,
        "profile_url": url,
        "username": username,
        "display_name": display_name,
        "bio": bio,
        "followers": parse_number(followers_txt),
        "following": parse_number(following_txt),
        "likes": parse_number(likes_txt),
        "website_url": website_url,
        "debug_html_path": html_path,
        "debug_screenshot_path": shot_path,
        "error": None,
    }


# =================== VIDEO LINKS (+ pinned + rank) ===================

PINNED_HINTS = ["pinned", "sabitle", "sabitlendi", "sabit"]

def collect_video_links_from_profile(driver, max_videos: int) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen = set()

    def detect_pinned_for_anchor(a_el) -> bool:
        try:
            parent = a_el
            for _ in range(5):
                parent = parent.find_element(By.XPATH, "..")
                txt = (parent.text or "").strip().lower()
                if any(h in txt for h in PINNED_HINTS):
                    return True
        except Exception:
            pass
        return False

    for _ in range(PROFILE_SCROLL_STEPS):
        try:
            a_tags = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/video/"]')
            for a in a_tags:
                href = a.get_attribute("href")
                if not href or "/video/" not in href:
                    continue
                vurl = href.split("?")[0]
                if vurl in seen:
                    continue

                seen.add(vurl)
                is_pinned = detect_pinned_for_anchor(a)

                out.append({
                    "video_url": vurl,
                    "is_pinned": bool(is_pinned),
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
        time.sleep(1.8)

        if is_challenge_like(driver):
            wait_challenge_clears(driver, context="collect_video_links")

    return out[:max_videos]


# =================== SCRAPE VIDEO (+ extra) ===================

POSTED_AT_SELECTORS = [
    '[data-e2e="browse-post-time"]',
    '[data-e2e="video-create-time"]',
    'span[data-e2e="video-creation-time"]',
    'time',
]

COMMENTS_DISABLED_HINTS = [
    "comments are turned off",
    "comments have been turned off",
    "yorumlar kapalı",
    "yorumlar devre dışı",
]
# NOTE: Video duration is read from client-side HTML5 metadata.
# No interaction or manipulation is performed.
def get_video_duration_sec(driver) -> Optional[float]:
    js = """
    const v = document.querySelector('video');
    if (!v) return null;
    const d = v.duration;
    if (!d || !isFinite(d)) return null;
    return d;
    """
    try:
        d = driver.execute_script(js)
        if d is None:
            return None
        return float(d)
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

    cc = text_or_none(driver, 'strong[data-e2e="comment-count"]') or text_or_none(driver, '[data-e2e="browse-comment-count"]')
    if cc is not None:
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
        m = re.search(r"(\d+\s*(gün|saat|dakika)\s*önce)", src, re.IGNORECASE)
        if m:
            return m.group(1)
        m = re.search(r"(\d+\s*(days?|hours?|minutes?)\s*ago)", src, re.IGNORECASE)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None

def scrape_video(driver, video_url: str, profile_username: str, is_pinned: bool, rank_on_profile: Optional[int]) -> Dict[str, Any]:
    ok = smart_get(driver, video_url, expected_css=VIDEO_EXPECTED, context=f"video_{profile_username}")
    if not ok:
        html_path, shot_path = save_debug(driver, f"video_fail_{profile_username}")
        return {
            "profile_username": profile_username,
            "video_url": video_url,
            "video_rank_on_profile": rank_on_profile,
            "is_pinned": is_pinned,
            "error": "video_nav_failed",
            "debug_html_path": html_path,
            "debug_screenshot_path": shot_path,
        }

    caption = (
        text_or_none(driver, '[data-e2e="browse-video-desc"]')
        or text_or_none(driver, 'h1[data-e2e="video-desc"]')
    )

    hashtags_list = extract_hashtags(caption)
    hashtag_count = len(hashtags_list) if hashtags_list else 0

    likes_txt = (
        text_or_none(driver, 'strong[data-e2e="like-count"]')
        or text_or_none(driver, '[data-e2e="browse-like-count"]')
    )
    comments_txt = (
        text_or_none(driver, 'strong[data-e2e="comment-count"]')
        or text_or_none(driver, '[data-e2e="browse-comment-count"]')
    )
    shares_txt = (
        text_or_none(driver, 'strong[data-e2e="share-count"]')
        or text_or_none(driver, '[data-e2e="browse-share-count"]')
    )
    views_txt = (
        text_or_none(driver, 'strong[data-e2e="play-count"]')
        or text_or_none(driver, '[data-e2e="browse-view-count"]')
    )

    music = (
        text_or_none(driver, '[data-e2e="browse-music"]')
        or text_or_none(driver, 'a[href*="/music/"]')
    )

    views = parse_number(views_txt)
    vlikes = parse_number(likes_txt)
    vcomments = parse_number(comments_txt)
    vshares = parse_number(shares_txt)

    posted_at_raw = find_posted_at(driver)
    posted_at_iso = try_parse_posted_at(posted_at_raw)

    video_duration_sec = get_video_duration_sec(driver)

    comments_enabled, comments_disabled_reason = detect_comments_enabled(driver)

    html_path, shot_path = save_debug(driver, f"video_{profile_username}")

    like_rate = (vlikes / views) if (views not in (None, 0) and vlikes is not None) else None
    engagement_rate = ((vlikes or 0) + (vcomments or 0) + (vshares or 0)) / views if (views not in (None, 0)) else None

    return {
        "profile_username": profile_username,
        "video_url": video_url,
        "video_rank_on_profile": rank_on_profile,
        "is_pinned": bool(is_pinned),

        "caption": caption,
        "hashtags": ",".join(hashtags_list) if hashtags_list else None,
        "hashtag_count": hashtag_count,
        "music_text": music,

        "posted_at_raw": posted_at_raw,
        "posted_at_iso": posted_at_iso,
        "video_duration_sec": video_duration_sec,

        "views": views,
        "video_likes": vlikes,
        "comments": vcomments,
        "shares": vshares,

        "like_rate": like_rate,
        "engagement_rate": engagement_rate,

        "comments_enabled": comments_enabled,
        "comments_disabled_reason": comments_disabled_reason,

        "debug_html_path": html_path,
        "debug_screenshot_path": shot_path,
        "error": None,
    }


# =================== LOAD USERS ===================

def load_users() -> List[str]:
    if not TXT_FILE.exists():
        return ["tiktok", "khaby.lame", "charlidamelio"]
    users = []
    with TXT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s:
                users.append(s)
    return users


# =================== FINALIZE EXCEL (robust) ===================

def finalize_excel():
    """
    FINAL ANALYSIS PIPELINE - SAĞLAMLAŞTIRILMIŞ VERSİYON
    """
    dfp = None
    dfv = None

    # 1. PROFILES YÜKLEME
    if PROFILES_CSV.exists():
        try:
            dfp = pd.read_csv(PROFILES_CSV, engine="python", on_bad_lines="skip")
            if dfp.empty:
                dfp = None
        except Exception as e:
            print(f"[HATA] Profiles CSV okunamadı: {e}")
            dfp = None

    # 2. VIDEOS YÜKLEME
    if VIDEOS_CSV.exists():
        try:
            dfv = pd.read_csv(VIDEOS_CSV, engine="python", on_bad_lines="skip")
            if dfv.empty:
                dfv = None
        except Exception as e:
            print(f"[HATA] Videos CSV okunamadı: {e}")
            dfv = None

    # EĞER PROFİL VERİSİ YOKSA İŞLEMİ DURDUR
    if dfp is None:
        print("[UYARI] İşlenecek profil verisi bulunamadı. Excel oluşturma durduruldu.")
        return

    # --- Profil İşlemleri (Buraya gelindiyse dfp vardır) ---
    if "normalized_username" not in dfp.columns and "username" in dfp.columns:
        dfp["normalized_username"] = dfp["username"]

    if "username" not in dfp.columns and "normalized_username" in dfp.columns:
        dfp["username"] = dfp["normalized_username"]

    if set(["followers", "likes"]).issubset(dfp.columns):
        dfp["like_per_follower"] = dfp.apply(
            lambda r: (r["likes"] / r["followers"])
            if pd.notna(r.get("followers")) and r.get("followers") not in (0, None)
            and pd.notna(r.get("likes"))
            else 0,
            axis=1
        )
    else:
        dfp["like_per_follower"] = 0

    if "category_confidence" not in dfp.columns:
        dfp["category_confidence"] = 50

    # --- Video Metriklerini Profile Ekleme ---
    if dfv is not None:
        if "engagement_rate" not in dfv.columns and \
           set(["views", "video_likes", "comments", "shares"]).issubset(dfv.columns):
            dfv["engagement_rate"] = dfv.apply(
                lambda r: (
                    (r.get("video_likes") or 0) +
                    (r.get("comments") or 0) +
                    (r.get("shares") or 0)
                ) / r["views"]
                if pd.notna(r.get("views")) and r.get("views") not in (0, None)
                else 0,
                axis=1
            )
        
        dfv["engagement_rate"] = dfv.get("engagement_rate", 0).fillna(0)

        if "profile_username" in dfv.columns:
            prof_eng = (
                dfv.groupby("profile_username", dropna=False)["engagement_rate"]
                .mean()
                .reset_index()
                .rename(columns={"engagement_rate": "avg_video_engagement"})
            )
            dfp = dfp.merge(
                prof_eng,
                left_on="normalized_username",
                right_on="profile_username",
                how="left"
            ).drop(columns=["profile_username"], errors="ignore")

    # --- Normalizasyon ve Skorlama ---
    dfp["avg_video_engagement"] = dfp.get("avg_video_engagement", 0).fillna(0)

    def normalize_series(s):
        s = pd.to_numeric(s, errors='coerce').fillna(0)
        if s.max() == s.min():
            return pd.Series([50] * len(s), index=s.index)
        return 100 * (s - s.min()) / (s.max() - s.min())

    dfp["followers"] = pd.to_numeric(dfp.get("followers", 0), errors='coerce').fillna(0)
    dfp["followers_log"] = np.log1p(dfp["followers"])

    dfp["n_engagement"] = normalize_series(dfp["avg_video_engagement"])
    dfp["n_followers"] = normalize_series(dfp["followers_log"])
    dfp["n_like_quality"] = normalize_series(dfp["like_per_follower"])
    dfp["n_category"] = normalize_series(dfp.get("category_confidence", 50))

    dfp["influencer_score"] = (
        0.45 * dfp["n_engagement"] +
        0.35 * dfp["n_followers"] +
        0.20 * dfp["n_like_quality"] 
    ).round(2)

    dfp.sort_values("influencer_score", ascending=False, inplace=True)

    # 3. EXPORT
    dfp.to_excel(DATA_DIR / "tiktok_profiles.xlsx", index=False)
    if dfv is not None:
        dfv.to_excel(DATA_DIR / "tiktok_videos.xlsx", index=False)

    print("✅ FINAL ANALYSIS & INFLUENCER SCORE HAZIR")

# ======================================================================
# ===================  CATEGORY MODULE (INTEGRATED)  ====================
# ======================================================================

OUT_PROFILES_CAT = DATA_DIR / "tiktok_profiles_categorized.xlsx"
OUT_VIDEOS_CAT = DATA_DIR / "tiktok_videos_categorized.xlsx"

MAX_VIDEOS_PER_PROFILE_FOR_CATEGORY = 10

W_HASHTAG = 3.0
W_CAPTION = 1.5
W_BIO = 1.0
W_MUSIC = 0.5

STOP_HASHTAGS = set([
    "fyp", "foryou", "foryoupage", "viral", "trend", "trending", "tiktok",
    "keşfet", "kesfet"
])

CATEGORIES: Dict[str, Dict[str, List[str]]] = {
    "Beauty & Personal Care": {"kw": [
        "makeup","skincare","beauty","cosmetics","glow","foundation","lipstick","hair","hairstyle","nail","perfume","routine",
        "makyaj","cilt","ciltbakım","ciltbakimi","kozmetik","saç","sac","bakım","bakim","parfüm","parfum","nemlendirici"
    ]},
    "Fashion & Style": {"kw": [
        "outfit","style","fashion","haul","trend","lookbook","wardrobe",
        "kombin","moda","stil","giyim","alışveriş","alisveris","dolap","tarz"
    ]},
    "Fitness & Health": {"kw": [
        "workout","gym","fitness","cardio","protein","strength","training","diet","health",
        "spor","antrenman","kas","kilo","diyet","sağlık","saglik"
    ]},
    "Food & Cooking": {"kw": [
        "recipe","cooking","food","chef","kitchen","mukbang","baking","dessert",
        "tarif","yemek","mutfak","aşçı","asci","pasta","tatlı","tatli","lezzet"
    ]},
    "Comedy & Entertainment": {"kw": [
        "funny","comedy","prank","joke","skit","meme","lol",
        "komedi","şaka","saka","eğlence","eglence","skeç","skec","mizah"
    ]},
    "Gaming": {"kw": [
        "gaming","gameplay","stream","streamer","esports","fortnite","valorant","minecraft","pubg","cs2",
        "league of legends","oyun","yayın","yayin","gamer"
    ]},
    "Technology & Digital": {"kw": [
        "tech","technology","software","ai","artificial intelligence","gadget","review","iphone","android","app","coding","python","data",
        "teknoloji","yapay zeka","yapayzeka","uygulama","kod","yazılım","yazilim","inceleme"
    ]},
    "Education & Informative": {"kw": [
        "tutorial","tips","how to","learn","education","explained","guide","lesson",
        "ders","eğitim","egitim","anlatım","anlatim","ipucu","nasıl","nasil","rehber"
    ]},
    "Travel & Lifestyle": {"kw": [
        "travel","trip","vlog","lifestyle","routine","daily","day in my life","morning",
        "gezi","seyahat","günlük","gunluk","rutin","hayat","yaşam","yasam"
    ]},
    "Music & Performance": {"kw": [
        "music","dance","singing","performance","cover","song","choreo",
        "müzik","muzik","dans","şarkı","sarki","performans"
    ]},
}

def _norm_text(x) -> str:
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return ""
    s = str(x).replace("\n"," ").replace("\r"," ")
    return s.lower().strip()

def _split_hashtags(hashtags_field: str) -> List[str]:
    s = _norm_text(hashtags_field)
    if not s:
        return []
    parts = [p.strip().lstrip("#") for p in s.split(",") if p.strip()]
    parts = [p for p in parts if p and p not in STOP_HASHTAGS]
    return parts

def _count_keyword_hits(text: str, keywords: List[str]) -> int:
    t = _norm_text(text)
    if not t:
        return 0
    hits = 0
    for kw in keywords:
        k = kw.lower().strip()
        if not k:
            continue
        if " " in k:
            if k in t:
                hits += 1
        else:
            if re.search(rf"\b{re.escape(k)}\b", t):
                hits += 1
    return hits

def _score_text(caption: str, hashtags: List[str], bio: str, music_text: str) -> Dict[str, float]:
    scores = {cat: 0.0 for cat in CATEGORIES.keys()}
    cap = _norm_text(caption)
    bio_t = _norm_text(bio)
    music_t = _norm_text(music_text)
    hashtag_text = " ".join([f"#{h}" for h in hashtags])

    for cat, spec in CATEGORIES.items():
        kw = spec["kw"]
        s = 0.0
        s += W_CAPTION * _count_keyword_hits(cap, kw)
        s += W_BIO * _count_keyword_hits(bio_t, kw)
        s += W_MUSIC * _count_keyword_hits(music_t, kw)
        s += W_HASHTAG * _count_keyword_hits(hashtag_text, kw)
        scores[cat] = s
    return scores

def _pick_top2(scores: Dict[str, float]) -> Tuple[str, str, float, float]:
    items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary, s1 = items[0]
    secondary, s2 = items[1] if len(items) > 1 else (None, 0.0)
    total = sum(v for _, v in items)
    conf = (s1 / total) if total > 0 else 0.0
    return primary, secondary, float(s1), float(conf)

def categorize_and_export():
    profiles_path = DATA_DIR / "tiktok_profiles.xlsx"
    videos_path = DATA_DIR / "tiktok_videos.xlsx"

    if not profiles_path.exists() or not videos_path.exists():
        print("[WARN] Categorization atlandı: input Excel bulunamadı.")
        return

    dfp = pd.read_excel(profiles_path)
    dfv = pd.read_excel(videos_path)

    if dfp.empty or dfv.empty:
        print("[WARN] Categorization atlandı: boş veri.")
        return
    dfp = pd.read_excel(profiles_path)
    dfv = pd.read_excel(videos_path)

    # Video-level category
    v_primary, v_secondary, v_score, v_conf = [], [], [], []
    for _, row in dfv.iterrows():
        tags = _split_hashtags(row.get("hashtags"))
        scores = _score_text(
            caption=row.get("caption"),
            hashtags=tags,
            bio="",
            music_text=row.get("music_text"),
        )
        p, s, top_score, conf = _pick_top2(scores)
        v_primary.append(p)
        v_secondary.append(s)
        v_score.append(top_score)
        v_conf.append(conf)

    dfv["category_primary_video"] = v_primary
    dfv["category_secondary_video"] = v_secondary
    dfv["category_score_video"] = v_score
    dfv["category_confidence_video"] = v_conf

    # Profile-level category (bio + last N videos)
    prof_key = "normalized_username" if "normalized_username" in dfp.columns else "username"
    vid_key = "profile_username" if "profile_username" in dfv.columns else None
    if not vid_key:
        print("[WARN] Categorization atlandı: videos dosyasında profile_username yok.")
        return

    g = dfv.groupby(vid_key, dropna=False)

    p_primary, p_secondary, p_score, p_conf = [], [], [], []
    for _, prow in dfp.iterrows():
        uname = prow.get(prof_key)
        bio = prow.get("bio", "")

        if uname in g.groups:
            vids = g.get_group(uname).head(MAX_VIDEOS_PER_PROFILE_FOR_CATEGORY)
        else:
            vids = dfv.iloc[0:0]

        agg = {cat: 0.0 for cat in CATEGORIES.keys()}

        # bio katkısı
        bio_scores = _score_text(caption="", hashtags=[], bio=bio, music_text="")
        for k, v in bio_scores.items():
            agg[k] += v

        # video katkısı
        for _, vrow in vids.iterrows():
            tags = _split_hashtags(vrow.get("hashtags"))
            scores = _score_text(
                caption=vrow.get("caption"),
                hashtags=tags,
                bio="",
                music_text=vrow.get("music_text"),
            )
            for k, v in scores.items():
                agg[k] += v

        p, s, top_score, conf = _pick_top2(agg)
        p_primary.append(p)
        p_secondary.append(s)
        p_score.append(top_score)
        p_conf.append(conf)

    dfp["category_primary"] = p_primary
    dfp["category_secondary"] = p_secondary
    dfp["category_score"] = p_score
    dfp["category_confidence"] = p_conf

    # düşük güven -> Mixed/Unclear
    dfp["category_primary_final"] = dfp.apply(
        lambda r: "Mixed/Unclear"
        if (r.get("category_confidence", 0) < CATEGORY_CONFIDENCE_THRESHOLD)
        else r.get("category_primary"),
        axis=1
    )

    dfp.to_excel(OUT_PROFILES_CAT, index=False)
    dfv.to_excel(OUT_VIDEOS_CAT, index=False)

    print("[DONE] Categorized profiles ->", OUT_PROFILES_CAT.resolve())
    print("[DONE] Categorized videos   ->", OUT_VIDEOS_CAT.resolve())


# =================== MAIN ===================

def main():
    users = load_users()
    state = load_state()

    done_users = set(state.get("done_users", []))
    done_videos = set(state.get("done_videos", []))

    print(f"[INFO] Users total: {len(users)} | already done: {len(done_users)}")
    print(f"[INFO] Chrome profile: {CHROME_PROFILE_DIR}")
    print(f"[INFO] Output: {DATA_DIR.resolve()}")
    print(f"[INFO] Video/Profile: {MAX_VIDEOS_PER_PROFILE} | Scroll steps: {PROFILE_SCROLL_STEPS}")

    driver = create_driver()

    try:
        smart_get(driver, "https://www.tiktok.com/", expected_css=['body'], context="home_boot")
        if is_challenge_like(driver):
            wait_challenge_clears(driver, context="home_boot")

        for idx, u in enumerate(users, start=1):
            uname = normalize_username(u)
            if uname in done_users:
                continue

            print(f"\n[STEP] {idx}/{len(users)} → {uname}")

            prof = scrape_profile(driver, u)
            append_csv_fixed(PROFILES_CSV, PROFILE_FIELDS, prof)

            if prof.get("error"):
                done_users.add(uname)
                state["done_users"] = sorted(done_users)
                save_state(state)
                jitter_sleep(SLEEP_BETWEEN_PROFILES)
                continue

            items = collect_video_links_from_profile(driver, MAX_VIDEOS_PER_PROFILE)
            print(f"[INFO] video links: {len(items)}")

            for item in items:
                vurl = item["video_url"]
                is_pinned = item.get("is_pinned", False)
                rank_on_profile = item.get("video_rank_on_profile")

                key = f"{uname}|{vurl}"
                if key in done_videos:
                    continue

                vrow = scrape_video(driver, vurl, uname, is_pinned=is_pinned, rank_on_profile=rank_on_profile)
                append_csv_fixed(VIDEOS_CSV, VIDEO_FIELDS, vrow)

                done_videos.add(key)
                state["done_videos"] = sorted(done_videos)
                save_state(state)

                jitter_sleep(SLEEP_BETWEEN_VIDEOS)

            done_users.add(uname)
            state["done_users"] = sorted(done_users)
            save_state(state)

            jitter_sleep(SLEEP_BETWEEN_PROFILES)

    finally:
        driver.quit()

    finalize_excel()
    categorize_and_export()

    print("\n[DONE] Excel created:")
    print(f" - {DATA_DIR / 'tiktok_profiles.xlsx'}")
    print(f" - {DATA_DIR / 'tiktok_videos.xlsx'}")
    print("\n[DONE] Categorized Excel created:")
    print(f" - {OUT_PROFILES_CAT}")
    print(f" - {OUT_VIDEOS_CAT}")
    print(f"\n[DONE] Debug folders: {RAW_HTML_DIR} | {SHOT_DIR}")
    print(f"[DONE] Checkpoint: {STATE_FILE}")


if __name__ == "__main__":
    main()