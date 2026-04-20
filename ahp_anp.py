# -*- coding: utf-8 -*-
"""
AHP (Analytic Hierarchy Process) ve ANP (Analytic Network Process)
Ağırlık Hesaplama Modülü
=================================================================
Lisans Tezi: "TikTok'ta Etkili Marka İş Birliği için İçerik Üreticisi
              Seçiminin Optimizasyonu"
Eskişehir Teknik Üniversitesi — Endüstri Mühendisliği

Bu modül, MCDM (Çok Kriterli Karar Verme) kriter ağırlıklarının
sistematik olarak hesaplanmasını sağlar.

AHP:  Saaty ölçeğinde (1-9) ikili karşılaştırma → eigen vector → ağırlıklar
ANP:  AHP + kriterler arası bağımlılık (inner dependence) → süper matris → ağırlıklar

Kriterler:
  C1: engagement_proxy    (Etkileşim Skoru)
  C2: followers           (Takipçi Büyüklüğü)
  C3: like_per_follower   (Takipçi Başına Beğeni)
  C4: cost_efficiency     (Maliyet Etkinliği)
  C5: video_volume        (Video Hacmi)
"""

import numpy as np
from typing import Dict, Tuple, List, Optional


# =====================================================================
# KRİTER İSİMLERİ
# =====================================================================

CRITERIA_NAMES = [
    "engagement_proxy",     # C1: Etkileşim Skoru
    "followers",            # C2: Takipçi Büyüklüğü
    "like_per_follower",    # C3: Takipçi Başına Beğeni
    "cost_efficiency",      # C4: Maliyet Etkinliği
    "video_volume",         # C5: Video Hacmi
]

CRITERIA_LABELS_TR = {
    "engagement_proxy":  "Etkileşim Skoru",
    "followers":         "Takipçi Büyüklüğü",
    "like_per_follower": "Takipçi Başına Beğeni",
    "cost_efficiency":   "Maliyet Etkinliği",
    "video_volume":      "Video Hacmi",
}

# Saaty Tutarlılık İndeksi (Random Index) — n=1..10
# Kaynak: Saaty, T. L. (1980). The Analytic Hierarchy Process.
RI_TABLE = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
            6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}


# =====================================================================
# AHP — Analytic Hierarchy Process
# =====================================================================

def build_default_pairwise_matrix() -> np.ndarray:
    """
    Varsayılan 5×5 AHP ikili karşılaştırma matrisi.

    Saaty Ölçeği:
      1   = Eşit önemde
      3   = Biraz daha önemli
      5   = Güçlü derecede önemli
      7   = Çok güçlü derecede önemli
      9   = Aşırı derecede önemli
      2,4,6,8 = Ara değerler

    Matris okuma:  satır_i / sütun_j = "i, j'ye göre ne kadar önemli?"

    Tasarım mantığı:
      - Etkileşim Skoru (C1) en önemli kriter
      - Takipçi Başına Beğeni (C3) ikinci sırada
      - Takipçi Büyüklüğü (C2) orta öneme sahip
      - Maliyet Etkinliği (C4) destek kriter
      - Video Hacmi (C5) en düşük ağırlıklı
    """
    #                     C1    C2    C3    C4    C5
    matrix = np.array([
        [1,     3,    2,    3,    5],     # C1: engagement_proxy
        [1/3,   1,    1/2,  2,    3],     # C2: followers
        [1/2,   2,    1,    2,    4],     # C3: like_per_follower
        [1/3,   1/2,  1/2,  1,    3],     # C4: cost_efficiency
        [1/5,   1/3,  1/4,  1/3,  1],     # C5: video_volume
    ], dtype=float)

    return matrix


def compute_ahp_weights(
    pairwise_matrix: np.ndarray,
    max_iter: int = 100,
    tol: float = 1e-8
) -> Dict:
    """
    AHP ağırlık hesaplama — Eigen Vector yöntemi.

    Parametre:
        pairwise_matrix : n×n ikili karşılaştırma matrisi (Saaty ölçeği)
        max_iter        : maksimum iterasyon sayısı
        tol             : yakınsama toleransı

    Dönen:
        {
            "weights"    : {kriter_adı: ağırlık},
            "weights_arr": np.ndarray,
            "lambda_max" : en büyük özdeğer,
            "ci"         : tutarlılık indeksi,
            "ri"         : rassal indeks,
            "cr"         : tutarlılık oranı (CR < 0.10 olmalı),
            "consistent" : bool (CR < 0.10 mi?)
        }
    """
    n = pairwise_matrix.shape[0]
    assert pairwise_matrix.shape == (n, n), "Matris kare olmalı"

    # ── Eigen vector hesaplama (üs yöntemi / power method) ───────────
    # Alternatif: np.linalg.eig kullanılabilir ama power method
    # daha kararlı ve anlaşılır.
    w = np.ones(n) / n  # başlangıç vektörü

    for _ in range(max_iter):
        w_new = pairwise_matrix @ w
        w_new = w_new / w_new.sum()  # normalize et
        if np.max(np.abs(w_new - w)) < tol:
            break
        w = w_new

    weights = w_new

    # ── Lambda_max (en büyük özdeğer) ────────────────────────────────
    # Aw = λ_max · w  →  λ_max = (Aw)_i / w_i  ortalama
    aw = pairwise_matrix @ weights
    lambda_max = np.mean(aw / weights)

    # ── Tutarlılık İndeksi (CI) ve Oranı (CR) ────────────────────────
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    ri = RI_TABLE.get(n, 1.49)
    cr = ci / ri if ri > 0 else 0.0

    # ── Sonuçları düzenle ────────────────────────────────────────────
    weight_dict = {}
    for i, name in enumerate(CRITERIA_NAMES[:n]):
        weight_dict[name] = round(float(weights[i]), 4)

    return {
        "weights":     weight_dict,
        "weights_arr": weights,
        "lambda_max":  round(float(lambda_max), 4),
        "ci":          round(float(ci), 4),
        "ri":          round(float(ri), 2),
        "cr":          round(float(cr), 4),
        "consistent":  cr < 0.10,
    }


def pairwise_from_sliders(slider_values: Dict[str, float]) -> np.ndarray:
    """
    Streamlit slider değerlerinden ikili karşılaştırma matrisi oluşturur.

    slider_values: {
        "C1_vs_C2": 3.0,   # C1, C2'ye göre 3 kat önemli
        "C1_vs_C3": 2.0,
        ...
    }

    Slider şeması (üst üçgen):
      (0,1), (0,2), (0,3), (0,4)
             (1,2), (1,3), (1,4)
                    (2,3), (2,4)
                           (3,4)
    Toplam: n*(n-1)/2 = 10 karşılaştırma (n=5 kriter için)
    """
    n = len(CRITERIA_NAMES)
    matrix = np.ones((n, n), dtype=float)

    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            key = f"C{i+1}_vs_C{j+1}"
            pairs.append((i, j, key))

    for i, j, key in pairs:
        val = slider_values.get(key, 1.0)
        if val >= 1:
            matrix[i, j] = val
            matrix[j, i] = 1.0 / val
        else:
            # val < 1 → j, i'ye göre daha önemli
            matrix[i, j] = val
            matrix[j, i] = 1.0 / val

    return matrix


def get_slider_pairs() -> List[Dict]:
    """
    Arayüzde gösterilecek karşılaştırma çiftlerini döner.

    Her çift:
        {
            "key": "C1_vs_C2",
            "label": "Etkileşim Skoru ↔ Takipçi Büyüklüğü",
            "left": "Etkileşim Skoru",
            "right": "Takipçi Büyüklüğü",
            "default": 3.0  (varsayılan matris değeri)
        }
    """
    default_matrix = build_default_pairwise_matrix()
    n = len(CRITERIA_NAMES)
    pairs = []

    for i in range(n):
        for j in range(i + 1, n):
            left_name = CRITERIA_LABELS_TR[CRITERIA_NAMES[i]]
            right_name = CRITERIA_LABELS_TR[CRITERIA_NAMES[j]]
            default_val = default_matrix[i, j]

            pairs.append({
                "key": f"C{i+1}_vs_C{j+1}",
                "label": f"{left_name} ↔ {right_name}",
                "left": left_name,
                "right": right_name,
                "default": round(float(default_val), 2),
                "i": i,
                "j": j,
            })

    return pairs


# =====================================================================
# ANP — Analytic Network Process
# =====================================================================

def build_default_inner_dependence() -> np.ndarray:
    """
    Kriterler arası iç bağımlılık (inner dependence) matrisi.

    ANP, AHP'den farklı olarak kriterler arasındaki etkileşimleri
    de modelleyebilir. Örneğin:
      - engagement_proxy ↔ like_per_follower (güçlü ilişki)
      - followers ↔ cost_efficiency (takipçi ↑ → maliyet ↑)
      - video_volume ↔ engagement_proxy (daha fazla video → daha fazla veri)

    Matris: n×n, her hücre ilgili kriterin diğerine etkisi (0-1 arası).
    Köşegen = 1 (kendi kendine etki).
    """
    #                          C1     C2     C3     C4     C5
    inner_dep = np.array([
        [1.00,  0.10,  0.60,  0.15,  0.20],   # C1 → diğerlerine etkisi
        [0.10,  1.00,  0.15,  0.50,  0.05],   # C2 → diğerlerine etkisi
        [0.60,  0.15,  1.00,  0.20,  0.10],   # C3 → diğerlerine etkisi
        [0.15,  0.50,  0.20,  1.00,  0.05],   # C4 → diğerlerine etkisi
        [0.20,  0.05,  0.10,  0.05,  1.00],   # C5 → diğerlerine etkisi
    ], dtype=float)

    return inner_dep


def compute_anp_weights(
    pairwise_matrix: np.ndarray,
    inner_dependence: Optional[np.ndarray] = None,
    max_power: int = 50,
    tol: float = 1e-8
) -> Dict:
    """
    ANP ağırlık hesaplama — Süper Matris yaklaşımı.

    ANP, AHP ağırlıklarını kriterler arası bağımlılıklarla düzeltir.

    Adımlar:
    1. AHP ile temel ağırlıkları hesapla (W_ahp)
    2. İç bağımlılık matrisini normalize et (D)
    3. Ağırlıklı süper matris oluştur: W_super = D_normalized × W_ahp_diag
    4. Limit süper matrisi hesapla: W_super^k (k→∞)
    5. Sonuç: kararlı haldeki ağırlıklar

    Parametreler:
        pairwise_matrix  : n×n AHP ikili karşılaştırma matrisi
        inner_dependence : n×n kriterler arası iç bağımlılık matrisi
        max_power        : süper matris üs alma iterasyon limiti
        tol              : yakınsama toleransı

    Dönen:
        {
            "weights"        : {kriter_adı: ağırlık},
            "weights_arr"    : np.ndarray,
            "ahp_weights"    : AHP ağırlıkları (karşılaştırma için),
            "adjustment"     : ANP düzeltme oranları,
            "supermatrix"    : limit süper matris
        }
    """
    n = pairwise_matrix.shape[0]

    # Adım 1: AHP ağırlıklarını hesapla
    ahp_result = compute_ahp_weights(pairwise_matrix)
    w_ahp = ahp_result["weights_arr"]

    if inner_dependence is None:
        inner_dependence = build_default_inner_dependence()

    # Adım 2: İç bağımlılık matrisini sütun-normalize et
    d_norm = inner_dependence.copy()
    for j in range(n):
        col_sum = d_norm[:, j].sum()
        if col_sum > 0:
            d_norm[:, j] = d_norm[:, j] / col_sum

    # Adım 3: Ağırlıklı süper matris oluştur
    # W_super = D_normalized × diag(W_ahp)
    w_super = d_norm @ np.diag(w_ahp)

    # Sütun normalize et
    for j in range(n):
        col_sum = w_super[:, j].sum()
        if col_sum > 0:
            w_super[:, j] = w_super[:, j] / col_sum

    # Adım 4: Limit süper matris hesapla (W^k → kararlı hal)
    w_limit = w_super.copy()
    for _ in range(max_power):
        w_new = w_limit @ w_limit
        # Sütun normalize et
        for j in range(n):
            col_sum = w_new[:, j].sum()
            if col_sum > 0:
                w_new[:, j] = w_new[:, j] / col_sum

        if np.max(np.abs(w_new - w_limit)) < tol:
            break
        w_limit = w_new

    # Adım 5: Kararlı ağırlıkları çıkar (herhangi bir sütun aynı)
    anp_weights = w_limit[:, 0]
    anp_weights = anp_weights / anp_weights.sum()

    # Düzeltme oranları
    adjustment = {}
    weight_dict = {}
    for i, name in enumerate(CRITERIA_NAMES[:n]):
        weight_dict[name] = round(float(anp_weights[i]), 4)
        ahp_w = float(w_ahp[i])
        anp_w = float(anp_weights[i])
        adj = ((anp_w - ahp_w) / ahp_w * 100) if ahp_w > 0 else 0.0
        adjustment[name] = round(adj, 2)

    return {
        "weights":      weight_dict,
        "weights_arr":  anp_weights,
        "ahp_weights":  ahp_result["weights"],
        "adjustment":   adjustment,
        "supermatrix":  w_limit,
    }


# =====================================================================
# YARDIMCI FONKSİYONLAR
# =====================================================================

def format_comparison_table(ahp_result: Dict, anp_result: Dict) -> List[Dict]:
    """
    AHP ve ANP ağırlıklarını karşılaştırma tablosu olarak formatlar.
    Streamlit'te pd.DataFrame olarak gösterilecek.
    """
    rows = []
    for name in CRITERIA_NAMES:
        ahp_w = ahp_result["weights"].get(name, 0)
        anp_w = anp_result["weights"].get(name, 0)
        adj   = anp_result["adjustment"].get(name, 0)

        rows.append({
            "Kriter": CRITERIA_LABELS_TR.get(name, name),
            "AHP Ağırlığı": f"{ahp_w:.4f}",
            "AHP (%)": f"%{ahp_w*100:.1f}",
            "ANP Ağırlığı": f"{anp_w:.4f}",
            "ANP (%)": f"%{anp_w*100:.1f}",
            "Fark (%)": f"{adj:+.1f}%",
        })

    return rows


def validate_pairwise_matrix(matrix: np.ndarray) -> Tuple[bool, str]:
    """
    İkili karşılaştırma matrisinin geçerliliğini kontrol eder.

    Kontroller:
    1. Kare matris
    2. Köşegen = 1
    3. a[i,j] = 1/a[j,i] (karşılıklılık)
    4. Pozitif değerler
    """
    n = matrix.shape[0]

    if matrix.shape[0] != matrix.shape[1]:
        return False, "Matris kare değil"

    for i in range(n):
        if abs(matrix[i, i] - 1.0) > 1e-6:
            return False, f"Köşegen[{i},{i}] = {matrix[i,i]:.2f}, 1 olmalı"

    for i in range(n):
        for j in range(i + 1, n):
            expected = 1.0 / matrix[i, j]
            if abs(matrix[j, i] - expected) > 0.01:
                return False, (
                    f"Karşılıklılık ihlali: M[{i},{j}]={matrix[i,j]:.2f} "
                    f"→ M[{j},{i}] = {matrix[j,i]:.2f}, beklenen = {expected:.2f}"
                )

    if np.any(matrix <= 0):
        return False, "Matristeki tüm değerler pozitif olmalı"

    return True, "Geçerli"


# =====================================================================
# TEST
# =====================================================================

if __name__ == "__main__":
    print("=" * 62)
    print("  AHP / ANP Ağırlık Hesaplama Testi")
    print("=" * 62)

    # AHP Test
    matrix = build_default_pairwise_matrix()
    print("\n📊 İkili Karşılaştırma Matrisi:")
    print(np.array2string(matrix, precision=2, suppress_small=True))

    valid, msg = validate_pairwise_matrix(matrix)
    print(f"\n✅ Matris geçerliliği: {msg}")

    ahp_result = compute_ahp_weights(matrix)
    print(f"\n📐 AHP Sonuçları:")
    print(f"  λ_max          : {ahp_result['lambda_max']}")
    print(f"  CI             : {ahp_result['ci']}")
    print(f"  RI             : {ahp_result['ri']}")
    print(f"  CR             : {ahp_result['cr']}")
    print(f"  Tutarlı mı?    : {'✅ Evet' if ahp_result['consistent'] else '❌ Hayır'}")
    print(f"\n  Ağırlıklar:")
    for name, w in ahp_result["weights"].items():
        label = CRITERIA_LABELS_TR.get(name, name)
        print(f"    {label:25s} : {w:.4f}  (%{w*100:.1f})")

    # ANP Test
    anp_result = compute_anp_weights(matrix)
    print(f"\n🔗 ANP Sonuçları (bağımlılık düzeltmeli):")
    print(f"  Ağırlıklar:")
    for name, w in anp_result["weights"].items():
        label = CRITERIA_LABELS_TR.get(name, name)
        adj = anp_result["adjustment"].get(name, 0)
        print(f"    {label:25s} : {w:.4f}  (%{w*100:.1f})  [{adj:+.1f}% düzeltme]")

    # Karşılaştırma tablosu
    print(f"\n📋 AHP vs ANP Karşılaştırma:")
    table = format_comparison_table(ahp_result, anp_result)
    for row in table:
        print(f"  {row['Kriter']:25s}  AHP={row['AHP (%)']:>6s}  "
              f"ANP={row['ANP (%)']:>6s}  Fark={row['Fark (%)']:>7s}")
