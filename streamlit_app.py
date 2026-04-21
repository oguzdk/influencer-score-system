import streamlit as st
import pandas as pd
import numpy as np
import os
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
except Exception as e:
    st.error(f"Optimizer import hatası: {e}")
    st.stop()

# Import AHP/ANP module
try:
    from ahp_anp import (
        compute_ahp_weights,
        build_default_pairwise_matrix,
        pairwise_from_sliders, get_slider_pairs,
        validate_pairwise_matrix,
        CRITERIA_NAMES, CRITERIA_LABELS_TR
    )
except Exception as e:
    st.error(f"AHP import hatası: {e}")
    st.stop()

st.set_page_config(
    page_title="TikTok Influencer Seçimi — AHP + Knapsack",
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
    .cr-ok { color: #22c55e; font-weight: bold; }
    .cr-bad { color: #ef4444; font-weight: bold; }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fafbfc 0%, #f0f2f6 100%);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📊 TikTok Influencer Marketing — Optimizasyon Sistemi</p>',
            unsafe_allow_html=True)
st.markdown("AHP Ağırlık Hesaplama • Gurobi ILP & Knapsack DP")
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

budget = st.sidebar.number_input(
    "💰 Maksimum Bütçe (TL)",
    min_value=1000, max_value=10000000, value=150000, step=10000
)

max_kisi = st.sidebar.number_input(
    "👥 Seçilecek Influencer Sayısı (0 = Sınırsız)",
    min_value=0, max_value=500, value=0, step=1,
    help="0 bırakırsanız bütçeye sığan en iyi kombinasyon seçilir."
)

st.sidebar.subheader("🔧 Algoritma Seçimi")
if GUROBI_AVAILABLE:
    algorithm = st.sidebar.radio(
        "Optimizasyon Yöntemi",
        ["Gurobi ILP", "Knapsack DP"],
        index=1,
        help="Gurobi: Akademik lisanslı tam çözücü | Knapsack: DP tabanlı"
    )
else:
    algorithm = "Knapsack DP"
    st.sidebar.info("ℹ️ Gurobi bulunamadı. Knapsack DP kullanılıyor.")

# Kategoriler
all_categories = sorted(list(df["category"].dropna().unique()))
selected_categories = st.sidebar.multiselect(
    "📂 Zorunlu Kategoriler (Opsiyonel)", all_categories
)

# Kara Liste
st.sidebar.subheader("🚫 Kara Liste")
all_users = sorted([u for u in df["username"].dropna().tolist() if str(u).strip()])
blacklist = st.sidebar.multiselect("Influencer Seç", all_users)


# =====================================================================
# SIDEBAR — AHP AĞIRLIK AYARLARI
# =====================================================================

st.sidebar.markdown("---")
st.sidebar.header("📐 AHP Ağırlık Hesaplama")

slider_pairs = get_slider_pairs()

ahp_use_custom = st.sidebar.checkbox("Özel AHP ağırlıkları kullan", value=True)

saaty_options = [
    "9 (Sol)", "8 (Sol)", "7 (Sol)", "6 (Sol)", "5 (Sol)", "4 (Sol)", "3 (Sol)", "2 (Sol)", 
    "1 (Eşit)", 
    "2 (Sağ)", "3 (Sağ)", "4 (Sağ)", "5 (Sağ)", "6 (Sağ)", "7 (Sağ)", "8 (Sağ)", "9 (Sağ)"
]

def map_val_to_opt(val):
    if val >= 1:
        v = int(round(val))
        return "1 (Eşit)" if v == 1 else f"{v} (Sol)"
    else:
        v = int(round(1/val))
        return f"{v} (Sağ)"

def map_opt_to_val(opt):
    if "Eşit" in opt:
        return 1.0
    v = int(opt.split()[0])
    return float(v) if "(Sol)" in opt else 1.0 / v

slider_values = {}
if ahp_use_custom:
    for pair in slider_pairs:
        default_opt = map_val_to_opt(float(pair["default"]))
        if default_opt not in saaty_options:
            default_opt = "1 (Eşit)"
        
        selected_opt = st.sidebar.select_slider(
            pair["label"],
            options=saaty_options,
            value=default_opt,
            key=pair["key"],
        )
        slider_values[pair["key"]] = map_opt_to_val(selected_opt)

# AHP Hesaplama
if ahp_use_custom and slider_values:
    ahp_matrix = pairwise_from_sliders(slider_values)
else:
    ahp_matrix = build_default_pairwise_matrix()

valid, valid_msg = validate_pairwise_matrix(ahp_matrix)
ahp_result = compute_ahp_weights(ahp_matrix)

# CR göstergesi
st.sidebar.markdown("---")
st.sidebar.subheader("📊 AHP Tutarlılık")
cr_val = ahp_result["cr"]
if ahp_result["consistent"]:
    st.sidebar.success(f"✅ CR = {cr_val:.4f} (< 0.10 → Tutarlı)")
else:
    st.sidebar.error(f"❌ CR = {cr_val:.4f} (≥ 0.10 → Tutarsız!)")

st.sidebar.markdown(f"**λ_max** = {ahp_result['lambda_max']}  |  **CI** = {ahp_result['ci']}")

active_weights = ahp_result["weights"]


# =====================================================================
# OPTİMİZASYON SONUÇLARI
# =====================================================================

btn_label = "🚀 Algoritmayı Çalıştır" + (f" ({max_kisi} Kişi)" if max_kisi > 0 else " (Sınırsız)")
if st.button(btn_label, type="primary", use_container_width=True):
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
                    label="Gurobi", verbose=False
                )
            else:
                ks_n = max_kisi if max_kisi > 0 else len(df)
                result = optimize_portfolio_knapsack(
                    df, budget_tl=budget,
                    n_select=ks_n,
                    required_categories=req_cats,
                    label="Knapsack", verbose=False,
                    criterion_weights=active_weights
                )

            if result["status"] in ["Optimal", "Suboptimal", "TimeLimit"]:
                st.success(f"✅ Optimizasyon Başarılı! ({algorithm} — {result['status']})")
                sel_df = result["selected"]
                n_sel = result["n_selected"]
                tot_cost = result["total_cost"]
                tot_score = result["total_score"]

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("👥 Kişi Sayısı", n_sel)
                col2.metric("💰 Harcanan Bütçe", f"{tot_cost:,.0f} TL",
                            f"{budget - tot_cost:,.0f} TL Kaldı", delta_color="normal")
                col3.metric("📊 Toplam MCDM Skoru", f"{tot_score:.2f}")
                col4.metric("🔧 Algoritma", algorithm)

                st.markdown("---")
                weight_str = " • ".join(
                    [f"{CRITERIA_LABELS_TR.get(k, k)}: %{v*100:.1f}"
                     for k, v in active_weights.items()]
                )
                st.caption(f"Ağırlıklar (AHP): {weight_str}")

                st.markdown("---")
                st.subheader(f"💡 Önerilen Influencerlar ({n_sel} Kişi)")

                grid_cols = st.columns(4)
                for idx, (_, row) in enumerate(sel_df.iterrows()):
                    with grid_cols[idx % 4]:
                        img_path = row.get("screenshot_cropped_path", "")
                        if pd.notna(img_path) and img_path and os.path.exists(str(img_path)):
                            img = Image.open(str(img_path))
                            st.image(img, caption="", use_container_width=True)
                        else:
                            st.info("Fotoğraf Bulunamadı")

                        st.markdown(f"### @{row['username']}")
                        st.markdown(f"**Kategori:** {row['category']}")
                        st.markdown(f"**Takipçi:** {row['followers']:,.0f}")
                        st.markdown(f"**Maliyet:** {row['estimated_cost_tl']:,.0f} TL")
                        st.markdown(f"**Skor:** {row['mcdm_score']:.3f}")
                        st.markdown("---")

            else:
                st.error(f"Optimizasyon başarısız oldu. Durum: {result['status']}.")
                st.info("Öneri: Bütçenizi artırmayı veya kısıtlamaları esnetmeyi deneyin.")

        except Exception as e:
            st.error(f"Hata oluştu: {e}")
            import traceback
            st.code(traceback.format_exc())
