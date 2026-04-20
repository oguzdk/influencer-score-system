# -*- coding: utf-8 -*-
"""
temizle_state.py  —  v2
========================
run_state.json'ı doğru şekilde sıfırlar.

SORUN (eski versiyon bunu kaçırıyordu):
  Chrome gece çöktüğünde scraper, done_users listesine kullanıcı adını
  yazıyordu ama profiles.csv'e hiç veri yazamıyordu. Dolayısıyla o
  ~400 kullanıcı "tamamlandı" sanılıp sonraki çalıştırmada atlanıyordu.

ÇÖZÜM:
  done_users = yalnızca profiles.csv'de HATASIZ kaydı olanlar
  Diğer herkes (hiç olmayan + hatalı) → tekrar denenecek

Kullanım:
  python temizle_state.py
"""

import json
import csv
import re
from pathlib import Path

DATA_DIR     = Path("data_tiktok")
STATE_FILE   = DATA_DIR / "run_state.json"
PROFILES_CSV = DATA_DIR / "profiles.csv"
TXT_FILE     = Path("tiktok_kullanicilar.txt")


def normalize(s: str) -> str:
    s = s.strip()
    if "tiktok.com" in s:
        m = re.search(r"@([^/?&#]+)", s)
        if m:
            return m.group(1).lower()
    return s.lstrip("@").lower()


def main():
    # 1. State oku
    if not STATE_FILE.exists():
        print(f"[UYARI] {STATE_FILE} bulunamadı.")
        return

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    done_users_old  = set(state.get("done_users",  []))
    done_videos_old = set(state.get("done_videos", []))

    print("=" * 55)
    print("  run_state.json Temizleyici  v2")
    print("=" * 55)
    print(f"  done_users (mevcut)  : {len(done_users_old)}")
    print(f"  done_videos (mevcut) : {len(done_videos_old)}")

    # 2. profiles.csv'den başarılı ve hatalıları ayır
    successfully_scraped = set()
    failed_in_csv        = set()

    if PROFILES_CSV.exists():
        with PROFILES_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                uname = normalize(row.get("normalized_username") or
                                  row.get("username") or "")
                if not uname:
                    continue
                err = (row.get("error") or "").strip()
                if err:
                    failed_in_csv.add(uname)
                else:
                    successfully_scraped.add(uname)
    else:
        print(f"  [UYARI] {PROFILES_CSV} bulunamadı — done_users tamamen sifirlanacak")

    print(f"\n  profiles.csv'de basarili : {len(successfully_scraped)}")
    print(f"  profiles.csv'de hatali   : {len(failed_in_csv)}")

    # Checkpoint'te olup CSV'de hiç bulunmayanlar
    missing_from_csv = done_users_old - successfully_scraped - failed_in_csv
    print(f"\n  Checkpoint'te var, veri YOK : {len(missing_from_csv)}")
    print(f"  Checkpoint'te var, hatali   : {len(failed_in_csv & done_users_old)}")
    print(f"  Checkpoint'te var, basarili : {len(successfully_scraped & done_users_old)}")

    to_retry = missing_from_csv | failed_in_csv
    print(f"\n  Yeniden denenecek TOPLAM : {len(to_retry)}")

    # 3. Yeni state: sadece başarılılar done sayılır
    new_done_users  = successfully_scraped
    new_done_videos = {v for v in done_videos_old
                       if not any(v.startswith(f"{u}|") for u in to_retry)}
    removed_videos  = len(done_videos_old) - len(new_done_videos)

    # 4. Yedek + kaydet
    backup = STATE_FILE.with_suffix(".json.bak")
    backup.write_text(STATE_FILE.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"\n  [YEDEK] {backup}")

    state["done_users"]  = sorted(new_done_users)
    state["done_videos"] = sorted(new_done_videos)
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print()
    print("=" * 55)
    print("  SONUC")
    print("=" * 55)
    print(f"  done_users  : {len(done_users_old):4d}  ->  {len(new_done_users):4d}"
          f"  ({len(to_retry)} kullanici sifirlandı)")
    print(f"  done_videos : {len(done_videos_old):4d}  ->  {len(new_done_videos):4d}"
          f"  ({removed_videos} video checkpoint silindi)")
    print()
    print("  Artik su komutu calistir:")
    print("  caffeinate -i python tiktok_scrapper_v3.py   (macOS)")
    print("  python tiktok_scrapper_v3.py                 (Windows)")
    print("=" * 55)


if __name__ == "__main__":
    main()