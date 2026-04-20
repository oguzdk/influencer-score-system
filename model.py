import pandas as pd
import pulp

# ---------------------------------------------------------
# 1. VERİ HAZIRLIĞI (Scraping Çıktısı)
# ---------------------------------------------------------
data = {
    'Influencer': ['Kişi_A', 'Kişi_B', 'Kişi_C', 'Kişi_D', 'Kişi_E', 'Kişi_F'],
    'Score': [85, 45, 75, 88, 92, 50],                # S_i (Etki Skoru)
    'Engagement': [0.05, 0.01, 0.04, 0.06, 0.09, 0.02], # E_i (Etkileşim Oranı)
    'Category_Match': [1.0, 0.5, 1.0, 0.5, 1.0, 0.0], # K_i (Kategori Uyumu)
    'Cost': [5000, 2000, 3000, 6000, 10000, 1500],    # C_i (Maliyet)
    'Category': ['Moda', 'Eğlence', 'Moda', 'Teknoloji', 'Eğlence', 'Teknoloji'] # I_k
}
df = pd.DataFrame(data)

# Amaç fonksiyonu için Toplam Değer hesaplaması
df['Total_Value'] = df['Score'] * df['Engagement'] * df['Category_Match']

# ---------------------------------------------------------
# 2. MODEL PARAMETRELERİ
# ---------------------------------------------------------
B = 3               # Maksimum Influencer Sayısı
E_min = 0.03        # Minimum Etkileşim Oranı (%3)
S_min = 60          # Minimum Influencer Skoru
Budget = 15000      # Toplam Bütçe

# Kategori Limitleri (Örn: Moda için en az 1, en fazla 2 kişi seç)
# Yapı: 'Kategori_Adı': (Minimum_M_k, Maksimum_L_k)
category_limits = {
    'Moda': (1, 2),
    'Eğlence': (1, 2),
    'Teknoloji': (0, 2)
}

# ---------------------------------------------------------
# 3. MODELİ TANIMLAMA
# ---------------------------------------------------------
model = pulp.LpProblem("TikTok_Influencer_Optimizasyonu", pulp.LpMaximize)
influencers = df['Influencer'].tolist()

# Kısıt 7: Karar Değişkeni (0 veya 1)
x = pulp.LpVariable.dicts("Secim", influencers, cat='Binary')

# ---------------------------------------------------------
# 4. AMAÇ FONKSİYONU
# ---------------------------------------------------------
# Max Z = Sum(S_i * E_i * K_i * x_i)
model += pulp.lpSum([df.loc[df['Influencer'] == i, 'Total_Value'].values[0] * x[i] for i in influencers]), "Toplam_Etkiyi_Maksimize_Et"

# ---------------------------------------------------------
# 5. MATEMATİKSEL KISITLARIN EKLENMESİ
# ---------------------------------------------------------

# Kısıt 1: Influencer Sayısı Kısıtı
model += pulp.lpSum([x[i] for i in influencers]) <= B, "Maksimum_Influencer_Sayisi"

# Kısıt 2 & 3: Minimum Etkileşim ve Minimum Skor Kısıtları
for i in influencers:
    e_i = df.loc[df['Influencer'] == i, 'Engagement'].values[0]
    s_i = df.loc[df['Influencer'] == i, 'Score'].values[0]
    
    # E_i * x_i >= E_min * x_i
    model += e_i * x[i] >= E_min * x[i], f"Min_Etkilesim_{i}"
    
    # S_i * x_i >= S_min * x_i
    model += s_i * x[i] >= S_min * x[i], f"Min_Skor_{i}"

# Kısıt 4 & 5: Minimum ve Maksimum Kategori Temsili Kısıtları
for cat, (m_k, l_k) in category_limits.items():
    cat_influencers = df[df['Category'] == cat]['Influencer'].tolist()
    
    # Sum(x_i) >= M_k (Minimum Temsiliyet)
    model += pulp.lpSum([x[i] for i in cat_influencers]) >= m_k, f"Min_Kategori_{cat}"
    
    # Sum(x_i) <= L_k (Kategori Çeşitliliği / Maksimum Yığılma)
    model += pulp.lpSum([x[i] for i in cat_influencers]) <= l_k, f"Max_Kategori_{cat}"

# Kısıt 6: Bütçe Kısıtı
model += pulp.lpSum([df.loc[df['Influencer'] == i, 'Cost'].values[0] * x[i] for i in influencers]) <= Budget, "Toplam_Butce_Kisiti"

# ---------------------------------------------------------
# 6. ÇÖZÜM VE SONUÇ RAPORLAMA
# ---------------------------------------------------------
model.solve()

print("--- OPTİMİZASYON SONUCU ---")
print("Çözüm Durumu:", pulp.LpStatus[model.status])

secilenler = []
toplam_maliyet = 0

for i in influencers:
    if x[i].varValue == 1.0:
        secilenler.append(i)
        maliyet = df.loc[df['Influencer'] == i, 'Cost'].values[0]
        toplam_maliyet += maliyet
        print(f"Seçildi: {i} (Maliyet: {maliyet} TL, Skor: {df.loc[df['Influencer'] == i, 'Score'].values[0]})")

print("-" * 25)
print(f"Maksimum Etki (Z): {pulp.value(model.objective):.4f}")
print(f"Harcanan Bütçe: {toplam_maliyet} TL / {Budget} TL")