import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from PIL import Image

# Import the existing optimization logic
try:
    from Tiktokoptimizerphase2v3gurobi import (
        load_data, apply_blacklist, estimate_costs,
        compute_mcdm_score, optimize_portfolio,
        optimize_portfolio_knapsack, build_engagement_proxy,
        GUROBI_AVAILABLE
    )
    import Tiktokoptimizerphase2v3gurobi
except ImportError as e:
    st.error(f"Tiktokoptimizerphase2v3gurobi import hatası: {e}")
    sys.exit(1)

# Import AHP/ANP module
try:
    from ahp_anp import (
        compute_ahp_weights, compute_anp_weights,
        build_default_pairwise_matrix, build_default_inner_dependence,
        pairwise_from_sliders, get_slider_pairs,
        format_comparison_table, validate_pairwise_matrix,
        CRITERIA_NAMES, CRITERIA_LABELS_TR
    )
except ImportError as e:
    st.error(f"ahp_anp import hatası: {e}")
    sys.exit(1)

st.set_page_config(
    page_title="TikTok Influencer Seçimi — AHP/ANP + Knapsack",
    page_icon="📊",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 800;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .cr-ok { color: #22c55e; font-weight: bold; }
    .cr-bad { color: #ef4444; font-weight: bold; }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fafbfc 0%, #f0f2f6 100%);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📊 TikTok Influencer Marketing — Optimizasyon Sistemi</p>',
            unsafe_allow_html=True)
st.markdown("AHP/ANP ağırlık hesaplama • Gurobi ILP & Knapsack DP • Her zaman 40 kişi seçimi")
st.markdown("---")


# =====================================================================
# VERİ YÜKLEME
# =====================================================================

@st.cache_data
def get_data():
    dfp, dfv = load_data()
    dfp = build_engagement_proxy(dfp, dfv)
    dfp = estimate_costs(dfp)
    dfp = compute_mcdm_score(dfp)
    return dfp

with st.spinner("Veriler yükleniyor..."):
    df = get_data()


# =====================================================================
# SIDEBAR — KAMPANYA AYARLARI
# =====================================================================

st.sidebar.header("⚙️ Kampanya Ayarları")

# ── 1. Bütçe ─────────────────────────────────────────────────────────
budget = st.sidebar.number_input(
    "💰 Maksimum Bütçe (TL)",
    min_value=1000, max_value=10000000, value=150000, step=10000
)

# ── 1b. Kişi Sayısı ──────────────────────────────────────────────────
max_kisi = st.sidebar.number_input(
    "👥 Seçilecek Influencer Sayısı (0 = Sınırsız)",
    min_value=0, max_value=500, value=0, step=1,
    help="0 bırakırsanız bütçeye sığan en iyi kombinasyon seçilir. Değer girerseniz tam o kadar kişi seçilmeye çalışılır."
)

# ── 2. Algoritma Seçimi ──────────────────────────────────────────────────
st.sidebar.subheader("🔧 Algoritma Seçimi")
if GUROBI_AVAILABLE:
    algorithm = st.sidebar.radio(
        "Optimizasyon Yöntemi",
        ["Gurobi ILP", "Knapsack DP"],
        index=1,
        help="Gurobi: Akademik lisanslı tam çözücü | Knapsack: DP tabanlı, harici bağımlılık yok"
    )
else:
    algorithm = "Knapsack DP"
    st.sidebar.info("ℹ️ Gurobi bulunamadı. Knapsack DP kullanılıyor.")

# ── 3. Kategoriler ───────────────────────────────────────────────────
all_categories = sorted(list(df["category"].dropna().unique()))
selected_categories = st.sidebar.multiselect(
    "📂 Zorunlu Kategoriler (Opsiyonel)",
    all_categories,
    help="En az bir kişinin bu kategorilerden seçilmesini zorunlu kılar."
)

# ── 4. Kara Liste ────────────────────────────────────────────────────
st.sidebar.subheader("🚫 Kara Liste")
all_users = sorted([u for u in df["username"].dropna().tolist() if str(u).strip()])
blacklist = st.sidebar.multiselect(
    "Influencer Seç",
    all_users,
    help="Seçtiğiniz profiller hiçbir şekilde algoritmaya dahil edilmeyecektir."
)

if len(blacklist) > 0:
    st.sidebar.write("Engellenenler:")
    cols = st.sidebar.columns(min(len(blacklist), 3))
    for i, user in enumerate(blacklist):
        row = df[df["username"] == user]
        if not row.empty:
            img_path = row.iloc[0]["screenshot_cropped_path"]
            col = cols[i % len(cols)]
            if pd.notna(img_path) and os.path.exists(img_path):
                img = Image.open(img_path)
                col.image(img, caption=user, width="stretch")
            else:
                col.write(f"{user}\n(Resim Yok)")


# =====================================================================
# SIDEBAR — AHP AĞIRLIK AYARLARI
# =====================================================================

st.sidebar.markdown("---")
st.sidebar.header("📐 AHP/ANP Ağırlık Hesaplama")
st.sidebar.markdown(
    "Saaty ölçeğinde (1-9) kriterler arası önem derecelerini belirleyin. "
    "Değer > 1 ise **sol kriter** daha önemlidir, < 1 ise **sağ kriter**."
)

# Slider'lar için kriter çiftlerini al
slider_pairs = get_slider_pairs()

# Slider değerlerini topla
ahp_use_custom = st.sidebar.checkbox(
    "Özel AHP ağırlıkları kullan",
    value=True,
    help="İşaretlenirse aşağıdaki slider değerleri kullanılır. Aksi halde varsayılan matris."
)

slider_values = {}

if ahp_use_custom:
    for pair in slider_pairs:
        # Slider: 1/9'dan 9'a kadar
        # Orta nokta (1.0) = eşit önemde
        val = st.sidebar.slider(
            pair["label"],
            min_value=1/9,
            max_value=9.0,
            value=float(pair["default"]),
            step=0.5,
            key=pair["key"],
            help=f"1 = Eşit | >1 = '{pair['left']}' daha önemli | <1 = '{pair['right']}' daha önemli"
        )
        slider_values[pair["key"]] = val

# ── AHP Hesaplama ────────────────────────────────────────────────────
if ahp_use_custom and slider_values:
    ahp_matrix = pairwise_from_sliders(slider_values)
else:
    ahp_matrix = build_default_pairwise_matrix()

# Matris geçerliliği
valid, valid_msg = validate_pairwise_matrix(ahp_matrix)

# AHP hesapla
ahp_result = compute_ahp_weights(ahp_matrix)

# ANP hesapla
inner_dep = build_default_inner_dependence()
anp_result = compute_anp_weights(ahp_matrix, inner_dep)

# ── Sidebar'da CR göstergesi ─────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.subheader("📊 AHP Tutarlılık")

cr_val = ahp_result["cr"]
if ahp_result["consistent"]:
    st.sidebar.markdown(
        f'<p class="cr-ok">✅ CR = {cr_val:.4f} (< 0.10 → Tutarlı)</p>',
        unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        f'<p class="cr-bad">❌ CR = {cr_val:.4f} (≥ 0.10 → Tutarsız! Karşılaştırmaları düzeltin.)</p>',
        unsafe_allow_html=True
    )

st.sidebar.markdown(f"**λ_max** = {ahp_result['lambda_max']}  |  **CI** = {ahp_result['ci']}")

# Hangi ağırlık setini kullanacağız?
weight_source = st.sidebar.radio(
    "Kullanılacak ağırlık yöntemi",
    ["AHP", "ANP"],
    index=0,
    help="AHP: Temel ikili karşılaştırma | ANP: Kriterler arası bağımlılıkla düzeltilmiş"
)

if weight_source == "AHP":
    active_weights = ahp_result["weights"]
else:
    active_weights = anp_result["weights"]


# =====================================================================
# ANA ALAN — AHP vs ANP KARŞILAŞTIRMA TABLOSU
# =====================================================================

tab_weights, tab_results = st.tabs(["📐 AHP/ANP Ağırlıklar", "💡 Optimizasyon Sonuçları"])

with tab_weights:
    st.subheader("AHP vs ANP Kriter Ağırlıkları Karşılaştırması")

    comparison_data = format_comparison_table(ahp_result, anp_result)
    comp_df = pd.DataFrame(comparison_data)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    # Ağırlık bar chart
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### AHP Ağırlıkları")
        ahp_chart_df = pd.DataFrame({
            "Kriter": [CRITERIA_LABELS_TR[c] for c in CRITERIA_NAMES],
            "Ağırlık": [ahp_result["weights"][c] for c in CRITERIA_NAMES]
        })
        st.bar_chart(ahp_chart_df.set_index("Kriter"), color="#667eea")

    with col_b:
        st.markdown("#### ANP Ağırlıkları")
        anp_chart_df = pd.DataFrame({
            "Kriter": [CRITERIA_LABELS_TR[c] for c in CRITERIA_NAMES],
            "Ağırlık": [anp_result["weights"][c] for c in CRITERIA_NAMES]
        })
        st.bar_chart(anp_chart_df.set_index("Kriter"), color="#764ba2")

    # İkili karşılaştırma matrisi göster
    with st.expander("📋 İkili Karşılaştırma Matrisi (AHP)"):
        matrix_labels = [CRITERIA_LABELS_TR[c] for c in CRITERIA_NAMES]
        matrix_df = pd.DataFrame(
            ahp_matrix,
            columns=matrix_labels,
            index=matrix_labels
        )
        st.dataframe(matrix_df.style.format("{:.2f}"), width="stretch")

    st.info(
        f"**Aktif ağırlık yöntemi: {weight_source}** — "
        f"Bu ağırlıklar optimizasyon çalıştırıldığında MCDM skorunu hesaplamak için kullanılacaktır."
    )


# =====================================================================
# ANA ALAN — OPTİMİZASYON SONUÇLARI
# =====================================================================

with tab_results:
    btn_label = "🚀 Algoritmayı Çalıştır" + (f" ({max_kisi} Kişi)" if max_kisi > 0 else " (Sınırsız)")
    if st.button(btn_label, type="primary", use_container_width=True):
        # Set the global blacklist so the script uses it
        Tiktokoptimizerphase2v3gurobi.BLACKLIST = blacklist

        with st.spinner(f"{algorithm} çözülüyor... Lütfen bekleyin."):
            try:
                req_cats = selected_categories if len(selected_categories) > 0 else None

                if algorithm == "Gurobi ILP":
                    gurobi_max = max_kisi if max_kisi > 0 else None
                    result = optimize_portfolio(
                        df, budget_tl=budget,
                        min_influencers=1,
                        max_influencers=gurobi_max,
                        required_categories=req_cats,
                        label="Gurobi",
                        verbose=False
                    )
                else:
                    # Knapsack DP
                    ks_n = max_kisi if max_kisi > 0 else len(df)
                    result = optimize_portfolio_knapsack(
                        df, budget_tl=budget,
                        n_select=ks_n,
                        required_categories=req_cats,
                        label="Knapsack",
                        verbose=False,
                        criterion_weights=active_weights
                    )

                if result["status"] in ["Optimal", "Suboptimal", "TimeLimit"]:
                    st.success(f"✅ Optimizasyon Başarılı! ({algorithm} — {result['status']})")
                    sel_df = result["selected"]
                    n_sel = result["n_selected"]
                    tot_cost = result["total_cost"]
                    tot_score = result["total_score"]

                    # ── Metrik Kartlar ─────────────────────────────────
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("👥 Kişi Sayısı", n_sel)
                    col2.metric("💰 Harcanan Bütçe", f"{tot_cost:,.0f} TL",
                                f"{budget - tot_cost:,.0f} TL Kaldı", delta_color="normal")
                    col3.metric("📊 Toplam MCDM Skoru", f"{tot_score:.2f}")
                    col4.metric("🔧 Algoritma", algorithm)

                    # ── Ağırlık bilgisi ────────────────────────────────
                    st.markdown("---")
                    st.markdown(f"**Kullanılan Ağırlık Yöntemi:** {weight_source}  |  "
                                f"**CR:** {ahp_result['cr']:.4f}  |  "
                                f"**Tutarlı:** {'✅' if ahp_result['consistent'] else '❌'}")

                    weight_str = " • ".join(
                        [f"{CRITERIA_LABELS_TR.get(k, k)}: %{v*100:.1f}"
                         for k, v in active_weights.items()]
                    )
                    st.caption(f"Ağırlıklar: {weight_str}")

                    st.markdown("---")
                    st.subheader(f"💡 Önerilen Influencerlar ({n_sel} Kişi)")

                    # ── Grid: 4 sütun ─────────────────────────────────
                    grid_cols = st.columns(4)
                    for idx, (_, row) in enumerate(sel_df.iterrows()):
                        with grid_cols[idx % 4]:
                            img_path = row.get("screenshot_cropped_path", "")
                            if pd.notna(img_path) and img_path and os.path.exists(str(img_path)):
                                img = Image.open(str(img_path))
                                st.image(img, caption="", width="stretch")
                            else:
                                st.info("Fotoğraf Bulunamadı")

                            # Information Card
                            st.markdown(f"### @{row['username']}")
                            st.markdown(f"**Kategori:** {row['category']}")
                            st.markdown(f"**Takipçi:** {row['followers']:,.0f}")
                            st.markdown(f"**Maliyet:** {row['estimated_cost_tl']:,.0f} TL")
                            st.markdown(f"**Skor:** {row['mcdm_score']:.3f}")
                            st.markdown("<br>", unsafe_allow_html=True)

                else:
                    st.error(f"Optimizasyon başarısız oldu. Durum: {result['status']}.")
                    st.info("Öneri: Bütçenizi artırmayı veya kategori kısıtlamalarını esnetmeyi deneyin.")

            except Exception as e:
                st.error(f"Hata oluştu: {e}")
                import traceback
                st.code(traceback.format_exc())
