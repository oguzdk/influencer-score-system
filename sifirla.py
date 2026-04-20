# -*- coding: utf-8 -*-
"""
sifirla.py
==========
Tüm scraper verilerini temizler ve sıfırdan başlamaya hazırlar.

SİLİNECEKLER:
  data_tiktok/profiles.csv
  data_tiktok/videos.csv
  data_tiktok/run_state.json
  data_tiktok/run_state.json.bak
  data_tiktok/tiktok_profiles.xlsx
  data_tiktok/tiktok_videos.xlsx
  data_tiktok/tiktok_profiles_categorized.xlsx
  data_tiktok/tiktok_videos_categorized.xlsx
  data_tiktok/raw_html/          (tüm debug HTML dosyaları)
  data_tiktok/screenshots/       (tüm ekran görüntüleri)

KORUNACAKLAR:
  tiktok_kullanicilar.txt        (kullanıcı listesi — dokunulmaz)
  chrome_profile/                (Chrome oturum bilgileri — dokunulmaz)

Kullanım:
  python sifirla.py
"""

import shutil
from pathlib import Path

DATA_DIR = Path("data_tiktok")

# Silinecek tek dosyalar
SINGLE_FILES = [
    DATA_DIR / "profiles.csv",
    DATA_DIR / "videos.csv",
    DATA_DIR / "run_state.json",
    DATA_DIR / "run_state.json.bak",
    DATA_DIR / "tiktok_profiles.xlsx",
    DATA_DIR / "tiktok_videos.xlsx",
    DATA_DIR / "tiktok_profiles_categorized.xlsx",
    DATA_DIR / "tiktok_videos_categorized.xlsx",
]

# Silinecek klasörler (içindekilerle birlikte)
FOLDERS = [
    DATA_DIR / "raw_html",
    DATA_DIR / "screenshots",
]


def fmt_size(path: Path) -> str:
    """Klasör/dosya boyutunu okunabilir formatta döner."""
    if path.is_file():
        b = path.stat().st_size
    elif path.is_dir():
        b = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    else:
        return "0 B"
    for unit in ["B", "KB", "MB", "GB"]:
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} TB"


def count_files(folder: Path) -> int:
    return sum(1 for _ in folder.rglob("*") if _.is_file()) if folder.exists() else 0


def main():
    print("=" * 55)
    print("  TikTok Scraper — Tam Sıfırlama")
    print("=" * 55)

    if not DATA_DIR.exists():
        print(f"\n  '{DATA_DIR}' klasörü bulunamadı.")
        print("  Zaten temiz! Scraper'ı doğrudan çalıştırabilirsin.")
        return

    # Neyin silineceğini listele
    print("\n  Silinecek dosyalar:")
    total_size = 0
    items_found = []

    for f in SINGLE_FILES:
        if f.exists():
            size = fmt_size(f)
            print(f"    [DOSYA] {f}  ({size})")
            items_found.append(f)

    for folder in FOLDERS:
        if folder.exists():
            n    = count_files(folder)
            size = fmt_size(folder)
            print(f"    [KLASÖR] {folder}/  ({n} dosya, {size})")
            items_found.append(folder)

    if not items_found:
        print("    → Silinecek bir şey yok, zaten temiz.")
        return

    # Onay al
    print()
    print("  ⚠️  Bu işlem GERİ ALINAMAZ.")
    print("  Korunacaklar: tiktok_kullanicilar.txt  |  chrome_profile/")
    print()
    answer = input("  Devam etmek istiyor musun? (evet / hayir): ").strip().lower()

    if answer not in ("evet", "e", "yes", "y"):
        print("\n  İptal edildi. Hiçbir şey silinmedi.")
        return

    # Sil
    print()
    deleted = 0
    for item in items_found:
        try:
            if item.is_file():
                item.unlink()
                print(f"  ✓ Silindi: {item}")
                deleted += 1
            elif item.is_dir():
                n = count_files(item)
                shutil.rmtree(item)
                print(f"  ✓ Silindi: {item}/  ({n} dosya)")
                deleted += 1
        except Exception as e:
            print(f"  ✗ Silinemedi: {item}  → {e}")

    print()
    print("=" * 55)
    print(f"  TAMAMLANDI — {deleted} öğe silindi")
    print("=" * 55)
    print()
    print("  Artık sıfırdan başlamak için:")
    print("  caffeinate -i python tiktok_scrapper_v3.py   (macOS)")
    print("  python tiktok_scrapper_v3.py                 (Windows)")
    print()


if __name__ == "__main__":
    main()