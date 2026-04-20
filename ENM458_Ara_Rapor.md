# ENM458 ENDÜSTRİ MÜHENDİSLİĞİ BİTİRME PROJESİ II - ARA RAPOR
**Tez Başlığı:** TİKTOK’TA ETKİLİ MARKA İŞ BİRLİĞİ İÇİN İÇERİK ÜRETİCİSİ SEÇİMİNİN OPTİMİZASYONU
**Öğrenciler:** Esra ZEYREK, Abdullah Raif YILDIRIM, Oğuzhan DİKMEN
**Danışman:** Asst. Prof. Dr. Zeliha ERGÜL AYDIN

Bu rapor, ENM458 Endüstri Mühendisliği Bitirme Projesi II kılavuzundaki 1-6. hafta gereksinimleri (Ara Sınav Raporu) doğrultusunda hazırlanmıştır.

## 1. Proje Planının Gözden Geçirilmesi ve Revizyonu
İlk dönemde (ENM457) TikTok platformundan içerik üreticilerine ait profil ve video metrikleri Selenium tabanlı web kazıma (web scraping) yöntemleriyle elde edilmiş ve temizlenmiştir. İçerisinde bulunduğumuz ikinci dönemde (ENM458), elde edilen veriler ışığında optimizasyon modelinin kurulması ve bu modelin kullanıcı dostu bir arayüzle buluşturulması hedeflenmiştir. 
İlk altı haftalık süreçte proje planına uygun olarak ilerlenmiş; Gurobi Solver kullanılarak Tam Sayılı Doğrusal Programlama (ILP) modeli geliştirilmiş ve Streamlit kütüphanesi yardımıyla dinamik bir karar destek arayüzü oluşturulmuştur. Bu doğrultuda iş-zaman çizelgesine uygunluk sürmektedir ve B planına geçişi gerektirecek büyük bir aksaklık yaşanmamıştır.

## 2. Sistem/Problem Verilerinin Toplanması ve Analizinin Yapılması
İlk dönem toplanan TikTok metaverileri (takipçi sayısı, beğeni, video sayısı ve kategoriler), çalışmanın optimizasyon aşamasına hazırlanmak üzere ikinci dönemde çeşitli veri işleme adımlarından geçirilmiştir. 
Bu aşamada:
- **Etkileşim Vekili (Engagement Proxy):** İçerik üreticilerinin video başına ortalama beğeni sayıları (avg_video_likes) ve takipçi sayıları üzerinden normalize edilmiş bir etkileşim göstergesi oluşturulmuştur.
- **Tahmini Maliyetleme (Cost Estimation):** Influencerlar takipçi bazlı "Tier" (Nano, Micro, Mid, Macro, Mega) sınıflarına ayrılarak taban ücretler ve etkileşim başına oranlarla bütçe maliyet tahminleri (TL cinsinden) yapılmıştır. Kategorilere bağlı çarpanlar (Beauty: 1.15, Food: 0.95 vb.) da tasarıma dahil edilerek maliyet asimetrileri gerçekçi koşullara uyarlanmıştır.
- **Çok Kriterli Karar Verme (MCDM) Skorlaması:** Etkileşim oranı, takipçi büyüklüğü, maliyet etkinliği ve video hacmi gibi öznitelikler ağırlıklandırılarak her içerik üreticisi için nihai bir "Cazibe (MCDM) Skoru" üretilmiştir. 

## 3. Modelleme ve Çözüm Önerileri: Seçilen Yöntem
Karar vericinin (markanın) farklı bütçe kısıtları altında en iyi etkiyi (maksimum MCDM skorunu) yakalayabilmesini sağlamak amacıyla deterministik ve stokastik doğası gereği esnek olan **Tam Sayılı Doğrusal Programlama (Integer Linear Programming - ILP)** modeli seçilmiştir.

**Optimizasyon Altyapısı (Gurobi ILP Model):**
- **Amaç Fonksiyonu:** Seçilen içerik üreticilerinin kümülatif MCDM skorunu maksimize etmek.
- **Kısıtlar (Gerçekçi Koşullar):**
  - **Bütçe Kısıtı:** Seçilenlerin toplam maliyeti, hedeflenen bütçe (budget_tl) sınırını aşamaz.
  - **Çeşitlilik Kısıtları:** Modele minimum ve maksimum influencer seçim kısıtları tanımlanmıştır. Ayrıca "Kara Liste" (Blacklist) mekanizması eklenerek markanın çalışmak istemediği kullanıcıların kesin olarak model dışı bırakılması sağlanmıştır.
  - **Kategori Dağılımı:** Arayüz üzerinden zorunlu kılınan sektör temsilcilerinin çözüm portföyüne dahil edilmesi garanti altına alınmıştır.

Sistem çözücü motoru olarak, endüstriyel boyuttaki büyük ölçekli problemleri dahi saniyeler içerisinde çözebilme kapasitesine sahip olan ve akademik lisansla edinilen **Gurobi Solver (gurobipy)** seçilmiştir. Çıktılar ayrıca Streamlit üzerinden görsel bir gösterge paneli aracılığıyla son kullanıcıya sunulmaktadır.

## 4. Projenin Girişimcilik ve Yenilikçilik Açısından Katkısı
Projenin sadece teorik bir akademik çalışma olarak kalmaması amacıyla kurulan Streamlit arayüzü, markalar ve dijital pazarlama ajansları için pazarlanabilir özellikler barındırmaktadır. Sezgisel olarak ilerleyen influencer pazarlaması bütçe tahsisini, tamamen veri güdümlü ve optimizasyon temelli bir karar destek sistemine dönüştürdüğü için sektörde ciddi bir "inovasyon" vizyonuna sahiptir. Markalara ait kara liste uygulaması, değişen maliyet sınırları ve kategori zorunlulukları sayesinde doğrudan pazar ihtiyacına cevap veren ölçeklenebilir ve satılabilir bir üründür.

## 5. BM Sürdürülebilir Kalkınma Amaçları (SKA) ve Sürdürülebilirlik Etkileri
Geliştirilen sistemin teknolojik, çevresel ve sosyoekonomik etkileri Sürdürülebilir Kalkınma Amaçları (SKA) ile yakından ilişkilidir:
- **SKA 8 (İnsana Yakışır İş ve Ekonomik Büyüme):** Geliştirilen analitik model, yalnızca devasa kitleye sahip "Mega" influencerları değil, veri metrikleriyle performansı kanıtlanmış "Nano" ve "Micro" seviyedeki üreticileri ve daha niş kitlelere hitap eden KOBİ'leri de potansiyel işbirliklerine (ekosisteme) entegre edebilmektedir.
- **SKA 12 (Sorumlu Üretim ve Tüketim):** Şirketlerin ve ajansların dijital pazarlama kaynakları, tahmini etki hesabı (MCDM ve bütçe kullanımı performansı) gözetilerek değerlendirilmektedir. Sistem finansal tüketimin ve yatırımların israfını engelleyerek verimlilik tabanlı, ekonomik açıdan sorumlu bir davranış modelini desteklemektedir. 

## 6. Gelecek Planı (Hafta 7-14)
Önümüzdeki haftalarda modelin farklı algoritmalar/parametreler üzerinden duyarlılık analizlerinin raporlanması, detaylı vaka (senaryo) çalışmalarının makale formatında sayısal olarak derinleştirilmesi ve dönemin nihai raporu için format düzenlemelerinin (tez kurallarına göre) yapılması planlanmaktadır.
