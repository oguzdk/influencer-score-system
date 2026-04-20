# TİKTOK'TA ETKİLİ MARKA İŞ BİRLİĞİ İÇİN İÇERİK ÜRETİCİSİ SEÇİMİNİN OPTİMİZASYONU

**Lisans Tezi**

**Esra ZEYREK
Abdullah Raif YILDIRIM
Oğuzhan DİKMEN**

**Eskişehir, 2026**

---

**Danışman: Asst. Prof. Dr. Zeliha ERGÜL AYDIN**

Eskişehir Teknik Üniversitesi Mühendislik Fakültesi
Endüstri Mühendisliği Bölümü
**Nisan, 2026**

---

## ÖZET

**TİKTOK'TA ETKİLİ MARKA İŞ BİRLİĞİ İÇİN İÇERİK ÜRETİCİSİ SEÇİMİNİN OPTİMİZASYONU**

**Esra ZEYREK | Abdullah Raif YILDIRIM | Oğuzhan DİKMEN**

Endüstri Mühendisliği
Eskişehir Teknik Üniversitesi, Mühendislik Fakültesi, Nisan, 2026
Danışman: Asst. Prof. Dr. Zeliha ERGÜL AYDIN

Dijital pazarlama ekosisteminde kısa video temelli içeriklerin önem kazanması, özellikle TikTok platformunu marka iletişim stratejilerinin merkezine taşımıştır. Ancak influencer seçimi çoğu zaman takipçi sayısı gibi sınırlı göstergelere dayandırılmakta, bu durum reklam bütçelerinin etkin kullanılamamasına ve yanlış hedef kitle eşleşmelerine neden olmaktadır.

Bu çalışma, TikTok üzerinde gerçekleştirilecek marka iş birlikleri için veri temelli ve matematiksel bir içerik üreticisi seçim modeli geliştirmeyi amaçlamaktadır. Birinci dönemde (ENM457) Selenium tabanlı web kazıma yöntemiyle içerik üreticilerine ait profil ve video metrikleri toplanmış; bu veriler ön işleme ve keşifsel analizden geçirilmiştir. İkinci dönemde (ENM458) ise toplanan verilen üzerinden etkileşim vekilleri (engagement proxy) hesaplanmış, takipçi bazlı kademeli bir maliyet tahmin modeli kurulmuş ve çok kriterli karar verme (MCDM) skoru üretilmiştir. Elde edilen bu sayısal göstergeler, Gurobi çözücüsü kullanılarak kurulan 0-1 Tam Sayılı Doğrusal Programlama (ILP) modeline girdi olarak aktarılmıştır. Model; bütçe kısıtı, minimum çeşitlilik, kategori dengesi ve kara liste toleransı gibi gerçekçi iş koşullarını barındırmakta ve Streamlit tabanlı interaktif bir karar destek arayüzü ile son kullanıcıya sunulmaktadır.

Elde edilen bulgular, modelin farklı bütçe senaryolarında tutarlı ve anlamlı influencer portföyleri önerdiğini, takipçi büyüklüğü yerine etkileşim kalitesini ön plana alan çözümler ürettiğini ortaya koymaktadır. Bu yaklaşım, dijital reklam kaynaklarının daha sorumlu ve verimli kullanılmasına katkı sağlamakta; SKA 12: Sorumlu Üretim ve Tüketim ile SKA 8: İnsana Yakışır İş ve Ekonomik Büyüme hedefleriyle doğrudan ilişkilendirilmektedir.

**Anahtar Sözcükler:** TikTok, içerik üreticisi seçimi, influencer optimizasyonu, tam sayılı doğrusal programlama, MCDM, Gurobi, web kazıma, dijital pazarlama, karar destek sistemi, sorumlu tüketim

---

## ABSTRACT

**OPTIMIZATION OF CONTENT CREATOR SELECTION FOR EFFECTIVE BRAND COLLABORATIONS ON TIKTOK**

**Esra ZEYREK | Abdullah Raif YILDIRIM | Oğuzhan DİKMEN**

Department of Industrial Engineering
Eskisehir Technical University, Engineering Faculty, April, 2026
Supervisor: Asst. Prof. Dr. Zeliha ERGÜL AYDIN

The growing dominance of short-form video content has positioned TikTok as a central platform in brand communication strategies. However, influencer selection is often based on simplistic metrics such as follower count, leading to inefficient allocation of advertising budgets and poor audience alignment.

This study aims to develop a data-driven, mathematical content creator selection model for brand collaborations on TikTok. In the first phase (ENM457), profile and video-level engagement data were collected via Selenium-based web scraping and subjected to exploratory analysis. In the second phase (ENM458), engagement proxies were computed, a tiered cost estimation model was established, and a Multi-Criteria Decision Making (MCDM) score was generated for each creator. These indicators were fed into a 0-1 Integer Linear Programming (ILP) model solved with Gurobi, incorporating realistic business constraints such as budget limits, minimum diversity, category distribution, and blacklist filtering. The system is presented to end users through an interactive Streamlit-based decision support interface.

Results indicate that the model consistently generates meaningful influencer portfolio recommendations across different budget scenarios, prioritizing engagement quality over follower volume. The approach supports more responsible and efficient use of digital advertising resources, directly aligning with SDG 12: Responsible Consumption and Production and SDG 8: Decent Work and Economic Growth.

**Keywords:** TikTok, content creator selection, influencer optimization, integer linear programming, MCDM, Gurobi, web scraping, digital marketing, decision support system, responsible consumption

---

## İÇİNDEKİLER

1. [GİRİŞ](#1-giriş)
   - 1.1. [Literatür Taraması](#11-literatür-taraması)
   - 1.2. [Problemin Kısaca Tarifi](#12-problemin-kısaca-tarifi)
   - 1.3. [Projenin Girişimcilik ve Yenilikçilik Açısından Katkısı](#13-projenin-girişimcilik-ve-yenilikçilik-açısından-katkısı)
   - 1.4. [Projenin BM Sürdürülebilir Kalkınma Amaçları Kapsamında Etkileri](#14-projenin-bm-sürdürülebilir-kalkınma-amaçları-kapsamında-etkileri)
2. [TAM SAYILI DOĞRUSAL PROGRAMLAMA YÖNTEMİ](#2-tam-sayılı-doğrusal-programlama-yöntemi)
3. [UYGULANMASI: TİKTOK VERİSİYLE ILP MODELİNİN GELİŞTİRİLMESİ](#3-uygulanmasi-tiktok-veriyle-ilp-modelinin-geliştirilmesi)
   - 3.1. [Sistem ve Problem Hakkında Genel Bilgiler](#31-sistem-ve-problem-hakkında-genel-bilgiler)
   - 3.2. [Veri Setinin İkinci Döneme Hazırlanması: Analitik Dönüşüm Adımları](#32-veri-setinin-ikinci-döneme-hazırlanması-analitik-dönüşüm-adımları)
   - 3.3. [ILP Modelinin Uygulanması ve Gurobi Entegrasyonu](#33-ilp-modelinin-uygulanması-ve-gurobi-entegrasyonu)
   - 3.4. [Streamlit Tabanlı Karar Destek Arayüzü](#34-streamlit-tabanlı-karar-destek-arayüzü)
4. [SONUÇ VE ÖNERİLER](#4-sonuç-ve-öneriler)
- [KAYNAKÇA](#kaynakça)
- [EKLER](#ekler)

**Tablolar Dizini:**
- Tablo 3.1. MCDM Kriter Ağırlık Tablosu
- Tablo 3.2. Takipçi Bazlı Kademeli Maliyet Modeli
- Tablo 3.3. Kategori Maliyet Çarpanları
- Tablo E.1. İş-Zaman Çizelgesi
- Tablo E.2. Risk Yönetim Tablosu (B Planı)

---

## 1. GİRİŞ

Sosyal medya platformlarının küresel kullanıcı kitlesini hızla büyütmesi ve bu platformların gündelik yaşamdaki yerini güçlendirmesiyle birlikte, dijital pazarlama faaliyetleri de köklü bir dönüşüm sürecine girmiştir. Geleneksel reklam mecralarının yerini giderek daha fazla sosyal medya iletişimi alırken, içerik üreticileri (influencer'lar) bu yeni reklamcılık düzeninin merkezinde konumlanmaktadır. TikTok özelinde bakıldığında, kısa video formatının hızlı tüketim yapısı ve algoritmik içerik keşif mekanizması, platformu markalar için stratejik bir iletişim kanalına dönüştürmüştür.

Influencer pazarlamasının büyümesiyle birlikte, içerik üreticisi seçim süreci de giderek daha kritik bir karar noktasına evrilmiştir. Küresel ölçekte influencer pazarlaması hacminin 2023 yılı itibarıyla 21 milyar doları aştığı tahmin edilmektedir [3]. Bu büyüme, aynı zamanda bütçe verimsizliği, yanlış hedef kitle eşleşmesi ve ölçümleme güçlükleri gibi sorunları da beraberinde getirmektedir. Özellikle Türkiye ölçeğinde influencer seçimi çoğunlukla sezgisel değerlendirmelere, ajans ağlarına veya yalnızca takipçi sayısı gibi yüzeysel kriterlere dayandırılmaktadır.

Bu gerçeklik, projenin temel motivasyonunu oluşturmaktadır: influencer seçimini "veri temelli bir optimizasyon problemi" olarak yeniden tanımlamak. Çalışmanın birinci döneminde (ENM457), bu problemi çözmek için gereken veri altyapısı Selenium tabanlı web kazıma yöntemiyle oluşturulmuştur. TikTok'un Türkiye'de resmi API erişimine kapalı olması nedeniyle veriler herkese açık profil sayfalarından sistematik biçimde toplanmış; profil bilgileri, video bazlı etkileşim metrikleri ve içerik tanımlayıcıları (hashtag, biyografi, kategori) bir araya getirilmiştir.

Çalışmanın ikinci dönemi olan ENM458 kapsamında ise bu ham veriler işlenmiş, analitik bileşenlere dönüştürülmüş ve nihayet bir optimizasyon modeline entegre edilmiştir. Gurobi akademik lisansıyla çözülen 0-1 Tam Sayılı Doğrusal Programlama (ILP) modeli, markanın bütçe kısıtları ve stratejik tercihleri doğrultusunda en yüksek performanslı influencer portföyünü otomatik olarak belirlemektedir. Sistem, Streamlit çerçevesiyle geliştirilen interaktif bir karar destek arayüzüyle son kullanıcıya sunulmaktadır.

Bu rapor, ENM458 Ara Sınav Raporunu (1-6. haftalar) kapsamakta olup modelin dayandığı yöntemi, veri hazırlık sürecini ve gerçekleştirilen uygulamayı bütünleşik biçimde aktarmaktadır.

---

### 1.1. Literatür Taraması

Influencer pazarlaması, hem pazarlama hem de bilgisayar bilimi literatüründe giderek artan bir ilgi görmektedir. Johnson ve Alvarez [1], dijital içerik üreticilerinin markalar ile tüketiciler arasında güven temelli bir köprü kurduğunu ve geleneksel reklamcılıktan farklı bir etkileşim yapısı sunduğunu belirtmektedir. Kumar ve Lee [2] ise içerik üreticisi pazarlamasının kullanıcı etkileşimi ve içerik özgünlüğü üzerine kurulu yapısını incelemiştir.

Zhang ve Han [3], influencer pazarlamasının teorik temellerini, güncel eğilimlerini ve gelecekteki araştırma yönlerini kapsamlı biçimde ele almıştır. Sektörün 2023 itibarıyla 21 milyar dolara ulaştığını vurgulayan bu çalışma, alanın akademik açıdan olgunlaşmakta olduğuna işaret etmektedir. Andersson ve Bergström [4] ise influencer başarısının yalnızca takipçi sayısıyla ölçülemeyeceğini; içerik kalitesi ve etkileşim yapısının da belirleyici olduğunu ampirik bulgularla ortaya koymuştur.

Bütçe kısıtlı optimizasyon yaklaşımları açısından Kim ve Cho [10], influencer kampanyalarının matematiksel modelleme ile optimize edilebileceğini göstermiştir. López-Dawn ve Giovanidis [11] ise influencer seçimini bütçe kısıtlı bir portföy optimizasyon problemi olarak ele alarak sistematik bir çözüme kavuşturmuştur. Ancak bu çalışmaların büyük çoğunluğu Instagram veya YouTube gibi platformlara odaklanmakta; TikTok'un kendine özgü algoritmik yapısını ve Türkiye koşullarını yansıtmamaktadır.

De Veirman ve arkadaşları [5], yüksek takipçi sayısının her zaman yüksek reklam etkisi anlamına gelmediğini göstermiştir. Bu bulgu, projemizin takipçi sayısı yerine etkileşim kalitesini merkeze alan tasarımını doğrudan desteklemektedir. Lou ve Yuan [6], influencer mesajlarının algılanan değeri ve güvenilirliğinin tüketici güvenini doğrudan etkilediğini belirtmiştir.

Hesaplamalı yaklaşımlar cephesinde Saito ve Kobayashi [7], influencer maksimizasyon problemini matematiksel bir çerçeveye taşımıştır. Tiukhova ve arkadaşları [8] ise dinamik grafik sinir ağları tabanlı bir yaklaşım önermiş; ancak bu tür karmaşık modellerin gerçek zamanlı iş dünyası uygulamalarına entegrasyonu güç olmaktadır. Li ve Wang [9], büyük veri analitiği ve ağ tabanlı yöntemlerin influencer etkinliğini anlamakta önemli katkılar sunduğunu ortaya koymuştur.

Tüm bu literatür tarandığında, TikTok verisine dayalı, Türkiye koşullarına özgü ve gerçekçi iş kısıtlarını içeren bir optimizasyon modelinin henüz geliştirilmediği görülmektedir. Bu çalışma, tam da bu boşluğu hedef alarak özgün bir katkı sunmayı amaçlamaktadır.

---

### 1.2. Problemin Kısaca Tarifi

Projenin çözdüğü problem şu şekilde özetlenebilir: Bir marka, belirli bir bütçe dahilinde TikTok'ta reklam kampanyası yürütmek istemektedir. Bütçesini en verimli şekilde kullanarak maksimum reklam etkisi yaratacak influencer kombinasyonunu nasıl seçmelidir?

Bu problem birden fazla alt bileşeni içermektedir:

**Veri Sorunu:** TikTok, Türkiye'de resmi API erişimi sunmamaktadır. Bu nedenle influencer verileri (takipçi sayısı, video beğeni ortalamaları, etkileşim oranları, içerik kategorileri) özgün web kazıma araçlarıyla toplanmak zorundadır.

**Ölçüm Sorunu:** Bir influencer'ın "ne kadar iyi" olduğunu tek bir sayıyla ifade etmek mümkün değildir. Bunu çözmek için çok kriterli bir değerlendirme skoru (MCDM skoru) geliştirilmiştir.

**Maliyet Belirsizliği:** Influencer fiyatları kamuya açık değildir. Sektör benchmarkları ve takipçi kademeleri (Nano, Micro, Mid, Macro, Mega) kullanılarak gerçekçi bir maliyet tahmin modeli oluşturulmuştur.

**Karar Sorunu:** Yüzlerce aday arasından bütçeye uygun, kategorileri dengeli, etkileşim kalitesi yüksek bir portföy oluşturmak; NP-zor bir kombinatoryal optimizasyon problemidir. Bu sorun 0-1 ILP modeliyle çözülmüştür.

**Kullanılabilirlik Sorunu:** Modelin uygulama değeri yaratması için teknik olmayan son kullanıcıların da erişebileceği bir arayüze ihtiyaç vardır. Bu arayüz Streamlit ile geliştirilmiştir.

Problemin gerçekçi kısıtları şunlardır:
- **Ekonomik:** Reklam bütçesi sınırlıdır ve her influencer'ın maliyeti farklıdır.
- **Stratejik:** Marka, belirli kategorilerde (örn. Fitness, Comedy, Beauty) mutlaka temsilci istemektedir.
- **İtibar Yönetimi:** Marka, geçmiş olumsuz deneyimler nedeniyle bazı influencer'larla çalışmak istememektedir (kara liste).
- **Risk Yönetimi:** Tüm bütçenin tek bir büyük hesaba verilmesi hem finansal hem de PR riski taşımaktadır (çeşitlilik kısıtı).

---

### 1.3. Projenin Girişimcilik ve Yenilikçilik Açısından Katkısı

Bu proje, salt akademik bir çalışmanın sınırlarını aşarak ticarileşme potansiyeli yüksek bir girişim prototipi sunmaktadır.

**Pazar Boşluğu ve Fırsat:** Türkiye'deki dijital pazarlama ajanslarının büyük çoğunluğu, influencer seçimini spreadsheet'ler, kişisel bağlantılar ve sezgilerle yapmaktadır. Bu proje, söz konusu boşluğu dolduracak, matematiksel altyapıya dayanan, ölçeklenebilir ve yeniden kullanılabilir bir karar destek aracı sunmaktadır.

**SaaS Ürün Potansiyeli:** Geliştirilen Streamlit arayüzü, aylık abonelik modeliyle (B2B SaaS) dijital ajanslar ve markalara sunulabilecek bir minimum uygulanabilir ürün (MVP) niteliği taşımaktadır. Kullanıcı, bütçesini ve tercihlerini girerek saniyeler içinde optimize edilmiş bir influencer listesi alabilmektedir.

**Yenilikçi Unsurlar:**
- Türkiye'de TikTok verisine dayalı ilk optimizasyon modeli olma özelliği
- API erişimi gerektirmeyen, web kazıma tabanlı özgün veri toplama altyapısı
- Takipçi sayısı yerine etkileşim kalitesini ön plana alan MCDM skorlama sistemi
- Gerçek zamanlı senaryo simülasyonu (farklı bütçe, kategori ve kara liste kombinasyonları)
- Teknik bilgi gerektirmeyen, sezgisel kullanıcı arayüzü

**Disiplinler Arası Yaklaşım:** Proje, Endüstri Mühendisliği (optimizasyon modeli), Bilgisayar Mühendisliği (web kazıma, Streamlit uygulaması) ve İşletme (pazarlama stratejisi, maliyet modeli) disiplinlerini başarıyla entegre etmektedir. Bu multidisipliner yapı, çözümün hem teknik derinliğini hem de pratik uygulama değerini artırmaktadır.

---

### 1.4. Projenin BM Sürdürülebilir Kalkınma Amaçları Kapsamında Etkileri

**SKA 8 — İnsana Yakışır İş ve Ekonomik Büyüme:**

Dijital reklam dünyasındaki mevcut yapıda, reklam harcamalarının büyük bölümü "Mega" düzeydeki (1 milyondan fazla takipçili) içerik üreticilerinde yoğunlaşmaktadır. Bu durum, organik etkileşim oranları yüksek, ancak henüz tanınmamış "Nano" (0-10 bin takipçi) ve "Micro" (10 bin-100 bin takipçi) düzeydeki yaratıcıların ekosistemin dışında kalmasına neden olmaktadır.

Geliştirilen optimizasyon modeli, maliyet etkinliği kriterini sisteme dahil ederek bu dengesizliği düzeltmektedir. Yüksek etkileşim kalitesine sahip küçük ölçekli içerik üreticileri, yalnızca takipçi sayısı kriteri yerine çok boyutlu bir değerlendirmeden geçirildiğinde algoritma tarafından öne çıkarılabilmektedir. Böylece dijital içerik ekonomisindeki fırsatlar daha geniş bir üretici kitlesine yayılmakta; KOBİ'ler ve yerel markalar da uygun maliyetli ama etkili işbirliği yapma imkânı bulmaktadır.

**SKA 12 — Sorumlu Üretim ve Tüketim:**

Dijital reklam bütçelerinin sezgisel kararlar veya tekil metriklerle tahsis edilmesi, kaynakların israfına ve başarısız kampanyaların tekrarlanmasına yol açmaktadır. Her başarısız kampanya hem finansal kayıp hem de gereksiz dijital içerik üretimiymiş enerji tüketimi anlamına gelmektedir.

Bu proje, her harcanan reklam lirasının matematiksel hesap görmeyi zorunlu kılan bir sistem kurmaktadır. MCDM skoru, bütçe kullanım oranı ve seçim gerekçeleri şeffaf ve sayısal biçimde sunulmaktadır. Bu yaklaşım; sorumlu tüketimi teşvik etmekte, başarısız kampanya sayısını azaltmakta ve dijital reklam sektöründe sürdürülebilir bir karar verme kültürünün yerleşmesine katkı sağlamaktadır.

---

## 2. TAM SAYILI DOĞRUSAL PROGRAMLAMA YÖNTEMİ

Tam Sayılı Doğrusal Programlama (Integer Linear Programming — ILP), karar değişkenlerinin tamsayı (tam sayı veya ikili 0-1) değerler almasını zorunlu kılan doğrusal optimizasyon problemlerinin çözümüne yönelik geliştirilmiş bir yöntemdir. ILP modelleri, hem amaç fonksiyonu hem de kısıtlar bakımından doğrusal ilişkiler içerdiğinden sistematik çözüm algoritmalarına elverişlidir. Karar değişkenlerinin tüm değil yalnızca tam sayı kümesinde aranması, özellikle "ya seçilir ya da seçilmez" tipindeki ikili karar problemleri için idealdir [10, 11].

**ILP'nin Bu Probleme Uygunluğu:**

Influencer seçim problemi, doğası gereği ikili bir karar yapısına sahiptir: bir influencer ya seçilir ($x_i = 1$) ya da seçilmez ($x_i = 0$). Bu yapı, problemi doğrudan 0-1 ILP'ye dönüştürmektedir. Sürekli çözüm yöntemlerine (LP relaxation) kıyasla ILP, gerçekçi ve uygulanabilir portföyler üretmesi bakımından üstündür. Kim ve Cho [10] ile López-Dawn ve Giovanidis [11], benzer yapıdaki influencer seçim problemlerini matematiksel programlama yöntemiyle çözmenin kampanya etkinliğini anlamlı biçimde artırdığını göstermiştir.

**Çözüm Algoritması — Gurobi Branch-and-Bound:**

Gurobi Solver, endüstriyel ölçekli optimizasyon problemleri için geliştirilmiş, akademik ve ticari kullanımda yaygın bir matematiksel programlama çözücüsüdür. Dal-ve-sınır (Branch-and-Bound) algoritması temelinde çalışan Gurobi, LP gevşemesi aracılığıyla tamsayılı çözümler için üst sınır hesaplamakta; ardından kural tabanlı dallara ayırma stratejileriyle arama alanını daraltmaktadır. Çoklu iş parçacığı (Threads=4) ve agresif ön-çözme (Presolve=2) parametreleriyle yapılandırılan model, birkaç yüz değişken içeren influencer problemlerini genellikle saniyeler içinde optimal ya da yakın-optimal biçimde çözmektedir.

**Yöntemin Sınırlılıkları ve Gerçekçi Değerlendirme:**

ILP modeli, belirlenen kısıtlar ve hedef fonksiyonu çerçevesinde matematiksel olarak optimal çözüm sunmaktadır. Ancak bu optimallik, modele yansıtılan varsayımlara bağımlıdır. Maliyet tahmin modeli gerçek fiyatların bir yaklaşımıdır; MCDM skoru geçmiş veri üzerinden türetilmiş olup gelecek performansı kesin olarak öngöremez. Bu sınırlılıklar, modelin bir ön eleme ve karar destek aracı olarak konumlandırılmasını ve uzman insan değerlendirmesiyle desteklenmesini gerektirmektedir.

---

## 3. UYGULANMASI: TİKTOK VERİSİYLE ILP MODELİNİN GELİŞTİRİLMESİ

### 3.1. Sistem ve Problem Hakkında Genel Bilgiler

Çalışma, TikTok platformunda marka iş birliği yapacak influencer'ların seçimini konu almaktadır. Türkiye'de 20 milyonu aşkın aktif TikTok kullanıcısı bulunmakla birlikte, platform Türkiye için resmi API erişimi sunmamaktadır. Bu durum, veri toplama sürecini doğrudan etkilemekte ve özgün mühendislik çözümleri gerektirmektedir.

Birinci dönemde (ENM457) yürütülen web kazıma süreci aracılığıyla Türkiye'deki çeşitli kategorilerde faaliyet gösteren içerik üreticilerine ait profil ve video verileri toplanmıştır. Elde edilen veri seti; kullanıcı adı, takipçi sayısı, toplam beğeni, video sayısı ve video bazlı etkileşim metrikleri (beğeni, yorum, paylaşım) ile kategori bilgilerini kapsamaktadır. içerik üreticileri Güzellik ve Bakım (Beauty & Personal Care), Moda ve Stil (Fashion & Style), Teknoloji ve Dijital (Technology & Digital), Yiyecek ve Yemek (Food & Cooking), Komedi ve Eğlence (Comedy & Entertainment), Spor ve Sağlık (Fitness & Health), Seyahat ve Yaşam (Travel & Lifestyle), Eğitim ve Bilgi (Education & Informative), Müzik ve Performans (Music & Performance) ile Oyun (Gaming) kategorileri altında sınıflandırılmıştır.

---

### 3.2. Veri Setinin İkinci Döneme Hazırlanması: Analitik Dönüşüm Adımları

Ham veri doğrudan optimizasyon modeline aktarılamaz. Bu nedenle birinci dönemde toplanan veriler, ikinci dönemde bir dizi analitik dönüşüm adımından geçirilmiştir.

#### 3.2.1. Etkileşim Vekili (Engagement Proxy) Hesaplanması

Yalnızca takipçi sayısına dayalı değerlendirmeler yanıltıcı olabilmektedir. Büyük kitleye ulaşabilen ancak düşük etkileşim oranına sahip hesaplar, marka iletişimi açısından sınırlı değer üretmektedir. Bu gerçekten yola çıkılarak, her içerik üreticisi için iki bileşenli bir "Etkileşim Vekili" skoru türetilmiştir:

**Bileşen 1 — Takipçi Başına Beğeni Oranı:**
$$like\_per\_follower_i = \frac{avg\_video\_likes_i}{\max(followers_i,\ 1)}$$

**Bileşen 2 — Ortalama Video Beğeni Logaritması:**
$$log\_avg\_likes_i = \ln(1 + avg\_video\_likes_i)$$

**Etkileşim Vekili (Normalize Edilmiş):**
$$engagement\_proxy_i = 0.60 \times \text{MinMax}(like\_per\_follower_i) + 0.40 \times \text{MinMax}(log\_avg\_likes_i)$$

%60 ağırlık, organik sadık kitleye sahip küçük üreticilerin adaletli biçimde temsil edilmesini sağlarken; %40 ağırlık, mutlak büyüklük avantajını da değerlendirmeye katmaktadır.

#### 3.2.2. Tahmini Maliyet Modeli (Cost Estimation Model)

TikTok işbirliği ücretleri kamuya açık değildir. Sektör benchmarkları ve akademik kaynaklara dayanan kademeli (Tier-based) bir maliyet modeli geliştirilmiştir. Model, her influencer için tahmini kampanya maliyetini takipçi büyüklüğü ve kategorisine göre hesaplamaktadır:

**Tablo 3.2. Takipçi Bazlı Kademeli Maliyet Modeli**

| Kademe (Tier) | Takipçi Aralığı | Taban Ücret | Artış Oranı |
|---------------|-----------------|-------------|-------------|
| Nano          | 0 – 10.000      | 1.500 TL    | 150 TL / 1K takipçi |
| Micro         | 10.000 – 100.000 | 8.000 TL   | 80 TL / 1K takipçi  |
| Mid           | 100.000 – 500.000 | 35.000 TL  | 35 TL / 1K takipçi  |
| Macro         | 500.000 – 1.000.000 | 90.000 TL | 20 TL / 1K takipçi  |
| Mega          | 1.000.000+      | 200.000 TL  | 8 TL / 1K takipçi   |

**Temel Maliyet Formülü:**
$$cost_i^{base} = TabanÜcret_{tier(i)} + \frac{followers_i}{1000} \times ArtışOranı_{tier(i)}$$

**Kategori Çarpanı Uygulaması:**

**Tablo 3.3. Kategori Maliyet Çarpanları**

| Kategori | Çarpan |
|----------|--------|
| Beauty & Personal Care | 1.15 |
| Fashion & Style | 1.10 |
| Technology & Digital | 1.05 |
| Travel & Lifestyle | 1.05 |
| Fitness & Health | 1.00 |
| Music & Performance | 1.00 |
| Mixed/Unclear | 1.00 |
| Food & Cooking | 0.95 |
| Comedy & Entertainment | 0.90 |
| Gaming | 0.90 |
| Education & Informative | 0.85 |

$$cost_i = cost_i^{base} \times CategoryMultiplier_{cat(i)}$$

#### 3.2.3. Çok Kriterli Karar Verme (MCDM) Skoru

Birden fazla kriterin bütünleşik biçimde değerlendirilmesi için ağırlıklı doğrusal birleştirme yöntemi kullanılmıştır. Her kriter önce Min-Max normalizasyonuyla $[0, 1]$ aralığına çekilmiş, ardından belirlenen ağırlıklarla ağırlıklı toplamı alınmıştır.

**Tablo 3.1. MCDM Kriter Ağırlık Tablosu**

| Kriter | Açıklama | Ağırlık |
|--------|----------|---------|
| Etkileşim Skoru | Engagement Proxy | %35 |
| Takipçi Büyüklüğü | log(1 + followers) | %20 |
| Takipçi Başına Beğeni | like_per_follower | %20 |
| Maliyet Etkinliği | log(avg_likes) / cost | %15 |
| Video Hacmi | video_count | %10 |

**MCDM Skoru Hesaplama Formülü:**
$$MCDM\_Score_i = 0.35 \cdot c1_i + 0.20 \cdot c2_i + 0.20 \cdot c3_i + 0.15 \cdot c4_i + 0.10 \cdot c5_i$$

Bu ağırlık yapısının temel tasarım mantığı şudur: etkileşim kalitesi (%35 + %20) en güçlü belirleyici unsur iken takipçi sayısının salt büyüklüğü tek başına yeterli kabul edilmemektedir. Maliyet etkinliği (%15) bütçe kullanımını optimize ederken video hacmi (%10) aktif içerik üretimini ödüllendirmektedir.

---

### 3.3. ILP Modelinin Uygulanması ve Gurobi Entegrasyonu

MCDM skorları ve maliyet tahminleri hesaplandıktan sonra, influencer seçim problemi bir 0-1 Tam Sayılı Doğrusal Programlama (ILP) modeli olarak kurulmuştur.

#### 3.3.1. Matematiksel Model Formülasyonu

**Karar Değişkeni:**
$$x_i \in \{0, 1\}, \quad \forall i \in \{1, 2, \ldots, n\}$$

- $x_i = 1$: $i$. içerik üreticisi portföye dahil edilir
- $x_i = 0$: $i$. içerik üreticisi seçilmez

**Amaç Fonksiyonu (Maksimizasyon):**
$$\text{Maximize} \quad Z = \sum_{i=1}^{n} MCDM\_Score_i \cdot x_i$$

**Kısıt 1 — Bütçe Kısıtı:**
$$\sum_{i=1}^{n} cost_i \cdot x_i \leq B$$

Seçilen influencer'ların toplam tahmini maliyeti, önceden belirlenen kampanya bütçesi $B$'yi aşamaz.

**Kısıt 2 — Minimum Çeşitlilik / Portföy Büyüklüğü:**
$$\sum_{i=1}^{n} x_i \geq n_{min}$$

Risk dağıtımı ve kampanya çeşitliliği için en az $n_{min}$ influencer seçimi zorunludur. Tüm bütçenin tek bir hesaba yatırılması hem finansal hem de PR riski taşımaktadır.

**Kısıt 3 — Maksimum Portföy Büyüklüğü (İsteğe Bağlı):**
$$\sum_{i=1}^{n} x_i \leq n_{max}$$

Yönetilebilirlik ve kampanya odağı açısından maksimum influencer sayısı sınırlandırılabilir.

**Kısıt 4 — Tier Bazlı Üst Sınır (İsteğe Bağlı):**
$$\sum_{i : tier(i) = t} x_i \leq L_t, \quad \forall t \in \{nano, micro, mid, macro, mega\}$$

Belirli bir kademedeki influencer sayısı sınırlandırılarak portföy risk dengesi yönetilir.

**Kısıt 5 — Zorunlu Kategori Temsili (İsteğe Bağlı):**
$$\sum_{i : category(i) = r} x_i \geq 1, \quad \forall r \in RequiredCategories$$

Kullanıcı tarafından belirlenen sektör kategorilerinden en az bir influencer seçilmesi sağlanır.

**Kısıt 6 — Kara Liste (Blacklist):**
$$x_k = 0, \quad \forall k \in \mathcal{K}_{black}$$

Kara listede yer alan influencer'lar ($\mathcal{K}_{black}$) hiçbir koşulda seçilmez. Bu kısıt, markanın itibar yönetimi kararlarını matematiksel garanti altına almaktadır.

#### 3.3.2. Gurobi Parametreleri ve Çözüm Süreci

Model aşağıdaki Gurobi parametre yapılandırmasıyla çözülmektedir:

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| TimeLimit | 60 sn | Maksimum çözüm süresi |
| MIPGap | 0.001 | %0.1 optimallik toleransı |
| Threads | 4 | Paralel iş parçacığı sayısı |
| MIPFocus | 1 | İyi çözüm bulmaya odaklan |
| Presolve | 2 | Agresif ön-çözme |

Model, optimal çözüme ulaştığında (GRB.OPTIMAL), zaman limitine yakın çözüm bulduğunda (GRB.TIME_LIMIT) veya uygulanabilir olmadığını tespit ettiğinde (GRB.INFEASIBLE) olmak üzere farklı sonuç durumlarını raporlamaktadır.

---

### 3.4. Streamlit Tabanlı Karar Destek Arayüzü

Gurobi modeli, `Tiktokoptimizerphase2v3gurobi.py` modülü içinde kapsüllenmiştir. Bu modül, `streamlit_app.py` aracılığıyla interaktif bir web uygulamasına entegre edilmektedir.

**Arayüz Özellikleri:**

- **Bütçe Slaydırı:** Kullanıcı, kampanya bütçesini 1.000 TL ile 10.000.000 TL arasında dinamik olarak belirleyebilir.
- **Kategori Seçimi:** Zorunlu kategori kısıtları çoklu seçim kutucuklarıyla tanımlanabilir.
- **Kara Liste Yönetimi:** İstenmediği düşünülen influencer'lar listeden seçilerek otomatik olarak model dışında tutulur. Kara listedeki hesapların profil görselleri de arayüzde görüntülenmektedir.
- **Sonuç Görüntüleme:** Optimizasyon çalıştırıldığında; seçilen kişi sayısı, harcanan bütçe, kalan bütçe ve toplam MCDM skoru metrik kartlarda özetlenmektedir. Seçilen influencer'lar ızgara (grid) düzeninde fotoğrafları, kategorileri, takipçi sayıları, tahmini maliyetleri ve MCDM skorlarıyla birlikte listelenmektedir.

Bu arayüz tasarımı, teknik bilgiden bağımsız olarak bir pazarlama yöneticisinin ya da ajans çalışanının modeli doğrudan kullanabilmesini sağlamaktadır.

---

## 4. SONUÇ VE ÖNERİLER

Bu çalışmanın ikinci dönem (ENM458) ilk altı haftasında gerçekleştirilen çalışmalar ve ulaşılan sonuçlar şu şekilde özetlenebilir:

Birinci dönemde Selenium tabanlı web kazıma yöntemiyle oluşturulan TikTok veri seti, ikinci dönemde analitik dönüşüm süreçlerinden geçirilerek optimizasyon modeline hazır hale getirilmiştir. Etkileşim vekili hesaplamaları, takipçi sayısının tek başına performansı açıklamadaki yetersizliğini bir kez daha doğrulamıştır; yüksek takipçili bazı hesapların, düşük takipçili ama etkileşim odaklı hesapların gerisinde MCDM skoru aldığı gözlemlenmiştir.

Gurobi ILP modeli, farklı bütçe senaryolarında (50K, 150K, 300K, 600K TL) tutarlı ve matematiksel olarak optimal portföyler üretmektedir. Model, geleneksel sezgisel yaklaşımların aksine, portföy bütçesini katmanlar arasında dengeleyerek hem maliyet etkinliğini hem de kategori çeşitliliğini optimize etmektedir.

**Sınırlılıklar:**
- Maliyet modeli, gerçek piyasa fiyatlarının sektör benchmarklarına dayanan bir tahminidir; bireysel pazarlık koşulları yansıtılmamıştır.
- Veri seti, yalnızca belirli bir zaman dilimini kapsamakta olup influencer performansı zaman içinde dalgalanabilmektedir.
- Web kazıma yöntemi yalnızca herkese açık profillerle sınırlıdır; gizli hesap verileri dahil edilememektedir.

**Sonraki Aşamada Planlanlar (Hafta 7–14):**
- Farklı bütçe seviyeleri ve kriter ağırlık kombinasyonları için kapsamlı duyarlılık analizi (Sensitivity Analysis) gerçekleştirilecektir.
- Modelin farklı marka profilleri (KOBİ, büyük ölçekli marka) için örnek vaka çalışmaları hazırlanacaktır.
- Streamlit arayüzüne senaryo karşılaştırma ve sonuç dışa aktarma (Excel/PDF) özellikleri eklenecektir.
- Tüm çalışma, ENM458 tez yazım kılavuzuna uygun biçimde formatlanarak nihai forma taşınacaktır.

---

## KAYNAKÇA

[1] Johnson, M., & Alvarez, L. (2021). The Rise of Digital Influencers: Shaping the Future of Marketing. *Journal of Digital Communication*, 14(3), 210–225.

[2] Kumar, R., & Lee, D. (2020). Influencer Marketing with Social Platforms. *Social Media Research Journal*, 8(4), 112–130.

[3] Zhang, P., & Han, Y. (2023). Social Media Influencer Marketing: Foundations, Trends and Research Directions. *International Journal of Marketing Science*, 19(1), 55–74.

[4] Andersson, S., & Bergström, E. (2020). Instagram and Influencer Marketing: An Empirical Study of the Parameters Behind Success. *Procedia Economics and Business*, 7(2), 89–101.

[5] De Veirman, M., Cauberghe, V., & Hudders, L. (2017). Marketing through Instagram influencers: The impact of number of followers and product divergence. *International Journal of Advertising*, 36(5), 798–828.

[6] Lou, C., & Yuan, S. (2019). Influencer marketing: How message value and credibility affect consumer trust. *Journal of Interactive Advertising*, 19(1), 58–73.

[7] Saito, M., & Kobayashi, K. (2019). A SI Model for Social Media Influencer Maximization. *IEEE Access*, 7, 150876–150889.

[8] Tiukhova, L., Korovin, D., & Melnikov, P. (2022). Influencer Prediction with Dynamic Graph Neural Networks. *Neural Networks*, 154, 145–159.

[9] Li, C., & Wang, H. (2022). Computational Studies in Influencer Marketing. *Expert Systems with Applications*, 193, 116–127.

[10] Kim, S., & Cho, Y. (2023). Optimal Influencer Marketing Campaign under Budget Constraints. *Journal of Business Analytics*, 12(3), 180–195.

[11] López-Dawn, A., & Giovanidis, A. (2021). Budgeted Portfolio Optimization Model for Social Media Influencer Selection. *Journal of Applied Optimization*, 18(4), 300–315.

[12] Araujo, T., Neijens, P., & Vliegenthart, R. (2019). Discovering Effective Influencers. *Computers in Human Behavior*, 98, 10–20.

[13] Phua, J., Jin, S. V., & Kim, J. (2020). The roles of celebrity endorsers' credibility and attractiveness in influencer marketing. *Computers in Human Behavior*, 102, 310–321.

[14] Influencer Marketing Hub. (2023). *Influencer Marketing Benchmark Report 2023*. Global Industry Review Series.

[15] Dwivedi, Y. K., et al. (2021). Setting the future of digital and social media marketing research. *International Journal of Information Management*, 59, 102168.

---

## EKLER

### Tablo E.1. İş-Zaman Çizelgesi

| No | İş Paketlerinin Adı | Zaman Aralığı | Takım Lideri | Ekip Üyeleri |
|----|---------------------|---------------|--------------|--------------|
| 1 | Veri Toplama Stratejisinin Belirlenmesi ve Ön Analiz | Ekim – Kasım 2025 | Esra Zeyrek | Abdullah Raif Yıldırım, Oğuzhan Dikmen |
| 2 | Kapsamlı Verinin Toplanması ve Veri Temizleme | Kasım – Aralık 2025 | Abdullah Raif Yıldırım | Esra Zeyrek, Oğuzhan Dikmen |
| 3 | Verilerin İşlenmesi ve Keşifsel İstatistiksel Analiz | Aralık 2025 – Ocak 2026 | Oğuzhan Dikmen | Abdullah Raif Yıldırım, Esra Zeyrek |
| 4 | Engagement Proxy, MCDM Skoru ve Maliyet Modeli Geliştirme | Ocak – Şubat 2026 | Abdullah Raif Yıldırım | Esra Zeyrek, Oğuzhan Dikmen |
| 5 | ILP Modelinin Kurulması, Gurobi Entegrasyonu ve Streamlit Arayüzü | Şubat – Mart 2026 | Esra Zeyrek | Abdullah Raif Yıldırım, Oğuzhan Dikmen |
| 6 | Senaryo Analizleri, Duyarlılık Testi ve Model Doğrulama | Nisan – Mayıs 2026 | Oğuzhan Dikmen | Abdullah Raif Yıldırım, Esra Zeyrek |
| 7 | Sonuçların Değerlendirilmesi, Raporlama ve Tez Yazımı | Mayıs 2026 | Esra Zeyrek | Abdullah Raif Yıldırım, Oğuzhan Dikmen |

---

### Tablo E.2. Risk Yönetim Tablosu (B Planı)

| No | En Büyük Riskler | Risk Yönetimi (B Planı) |
|----|------------------|--------------------------|
| 1 | TikTok'un veri erişimini kısıtlaması veya doğrulama mekanizmalarını artırması | İnsan davranışını taklit eden esnek scraper yapısı kullanılmaktadır. Kısıtlama artarsa veri çekme hızı azaltılacak, mevcut veri seti ek kaynaklar (alternatif platform verileri) ile zenginleştirilecektir. |
| 2 | Toplanan verinin analiz için yetersiz kalması | Başlangıç örneklemi genişletilebilir biçimde tasarlanmıştır. Yetersizlik durumunda kullanıcı sayısı artırılacak veya mevcut ağırlıklı normalize metrikler kullanılacaktır. |
| 3 | API eksikliği nedeniyle veri tutarlılığının sağlanamaması | Veriler yalnızca herkese açık kaynaklardan toplanmış, veri temizleme ve çapraz doğrulama ile tutarlılık güvence altına alınmıştır. |
| 4 | Web kazıma sürecinde teknik hatalar veya kesintiler yaşanması | Ara kayıt (checkpoint) mekanizmalarıyla veri kaybı önlenmiştir. Hata durumunda süreç kaldığı yerden devam edecek şekilde yapılandırılmıştır. |
| 5 | Optimizasyon modelinde uygulanabilir çözüm bulunamaması (infeasible) | Bütçe artırılacak, kategori kısıtları esnetilecek veya kara liste daraltılacaktır. Arayüz bu durumda kullanıcıya doğrudan öneride bulunmaktadır. |
| 6 | Gurobi lisans sorunları yaşanması | PuLP + CBC (açık kaynak) çözücüsüne geçiş B planı olarak hazır tutulmaktadır. Model bu geçişe uyumlu biçimde kodlanmıştır. |
| 7 | Zaman planına uyulamaması | İş paketleri paralel planlanmıştır. Gecikme durumunda kapsam daraltılarak temel model tutulacak, gelişmiş özellikler sonraki versiyona aktarılacaktır. |
