**TİKTOK'TA ETKİLİ MARKA İŞ BİRLİĞİ İÇİN İÇERİK ÜRETİCİSİ SEÇİMİNİN OPTİMİZASYONU**

**Lisans Tezi**

**Esra ZEYREK**

**Abdullah Raif YILDIRIM**

**Oğuzhan DİKMEN**

**Eskişehir, 2026**

**LİSANS TEZİ**

**Danışman: Asst. Prof. Dr. Zeliha ERGÜL AYDIN**

**Eskişehir Teknik Üniversitesi Mühendislik Fakültesi**

**Endüstri Mühendisliği Bölümü**

**Nisan, 2026**

---

## ÖZET

TİKTOK'TA ETKİLİ MARKA İŞ BİRLİĞİ İÇİN İÇERİK ÜRETİCİSİ SEÇİMİNİN OPTİMİZASYONU

Esra ZEYREK | Abdullah Raif YILDIRIM | Oğuzhan DİKMEN

Endüstri Mühendisliği

Eskişehir Teknik Üniversitesi, Mühendislik Fakültesi, Nisan, 2026

Danışman: Asst. Prof. Dr. Zeliha ERGÜL AYDIN

Dijital pazarlama faaliyetlerinin sosyal medya platformlarına kaymasıyla birlikte, içerik üreticileri markalar için önemli bir iletişim aracı hâline gelmiştir. Özellikle TikTok, kısa video formatı ve yüksek etkileşim oranları sayesinde marka iş birliklerinin yoğunlaştığı bir platform olarak öne çıkmaktadır. Ancak içerik üreticisi (influencer) seçimi çoğu zaman takipçi sayısı gibi sınırlı göstergelere dayandırılmakta, bu durum reklam bütçelerinin etkin kullanılmasını zorlaştırmaktadır.

Bu çalışma, TikTok üzerinde gerçekleştirilecek marka iş birlikleri için veri temelli ve matematiksel bir içerik üreticisi seçim modeli geliştirmeyi amaçlamaktadır. ENM457 (Bitirme Projesi I) kapsamında Selenium tabanlı web kazıma yöntemiyle içerik üreticilerine ait profil ve video metrikleri sistematik biçimde toplanmış; bu veriler ön işleme ve keşifsel analizden geçirilmiştir. ENM458 (Bitirme Projesi II) kapsamında ise her içerik üreticisi için etkileşim vekili (engagement proxy) hesaplanmış, takipçi kademeleri ve kategori çarpanlarına dayanan bir maliyet tahmin modeli oluşturulmuş ve çok kriterli karar verme (MCDM) skoru üretilmiştir. Bu sayısal göstergeler, Gurobi'nin akademik lisansıyla çözülen 0-1 Tam Sayılı Doğrusal Programlama (ILP) modeline girdi olarak aktarılmıştır. Model; bütçe kısıtı, minimum portföy çeşitliliği, kategori dengesi ve kara liste toleransı gibi gerçekçi iş koşullarını barındırmakta; Streamlit tabanlı interaktif bir karar destek arayüzü ile son kullanıcıya sunulmaktadır.

Elde edilen bulgular, modelin farklı bütçe senaryolarında tutarlı ve anlamlı influencer portföyleri önerdiğini, takipçi büyüklüğü yerine etkileşim kalitesine dayalı çözümler ürettiğini ortaya koymaktadır. Bu yaklaşım; dijital reklam kaynaklarının daha verimli kullanılmasına katkı sağlamakta ve Birleşmiş Milletler Sürdürülebilir Kalkınma Amaçlarından SKA 8: İnsana Yakışır İş ve Ekonomik Büyüme ile SKA 12: Sorumlu Üretim ve Tüketim hedefleriyle doğrudan ilişkilendirilmektedir.

**Anahtar Sözcükler:** TikTok, içerik üreticisi seçimi, influencer optimizasyonu, 0-1 tam sayılı doğrusal programlama, MCDM, Gurobi, web kazıma, dijital pazarlama, karar destek sistemi, sorumlu tüketim

---

## ABSTRACT

OPTIMIZATION OF CONTENT CREATOR SELECTION FOR EFFECTIVE BRAND COLLABORATIONS ON TIKTOK

Esra ZEYREK | Abdullah Raif YILDIRIM | Oğuzhan DİKMEN

Department of Industrial Engineering

Eskisehir Technical University, Engineering Faculty, April, 2026

Supervisor: Asst. Prof. Dr. Zeliha ERGÜL AYDIN

With the rapid expansion of social media platforms, content creators have become a central element of brand communication strategies. TikTok, in particular, has emerged as a dominant platform for brand collaborations due to its short-video format and high user engagement rates. However, influencer selection is frequently based on oversimplified indicators such as follower count, leading to inefficient use of advertising budgets and poor audience alignment.

This study develops a data-driven, mathematically grounded content creator selection model for TikTok-based brand collaborations. In the first phase (ENM457), profile and video-level engagement data were systematically collected via Selenium-based web scraping and subjected to exploratory analysis. In the second phase (ENM458), an engagement proxy was computed for each creator, a tiered cost estimation model was constructed using follower brackets and category multipliers, and a Multi-Criteria Decision Making (MCDM) score was derived. These quantitative indicators serve as inputs to a 0-1 Integer Linear Programming (ILP) model solved with Gurobi, incorporating realistic business constraints including budget limits, minimum portfolio diversity, category distribution requirements, and blacklist filtering. The system is delivered to end users through an interactive Streamlit-based decision support interface.

Results demonstrate that the model consistently produces meaningful influencer portfolio recommendations across diverse budget scenarios, prioritizing engagement quality over follower volume. The approach promotes more responsible and efficient use of digital advertising resources, directly aligning with SDG 8: Decent Work and Economic Growth and SDG 12: Responsible Consumption and Production.

**Keywords:** TikTok, content creator selection, influencer optimization, 0-1 integer linear programming, MCDM, Gurobi, web scraping, digital marketing, decision support system, responsible consumption

---

## İÇİNDEKİLER

1. GİRİŞ
2. PROBLEMİN TARİFİ
3. LİTERATÜR TARAMASI
   - 3.1. Genel Değerlendirme ve Tezin Literatürdeki Konumu
4. PROJENİN GİRİŞİMCİLİK VE YENİLİKÇİLİK AÇISINDAN KATKISI
   - 4.1. Projenin BM Sürdürülebilir Kalkınma Amaçları Kapsamında Topluma, Ekonomiye, Sürdürülebilirliğe ve Çevreye Etkileri
5. ÇALIŞMADA KULLANILAN TEMEL KAVRAMLAR VE YÖNTEMLER
   - 5.1. Veri Toplama Süreci ve Ön İşleme
   - 5.2. Analitik Dönüşüm Adımları
   - 5.3. Optimizasyon Modeli: 0-1 Tam Sayılı Doğrusal Programlama
   - 5.4. Streamlit Tabanlı Karar Destek Arayüzü
6. SONUÇ VE ÖNERİLER
7. KAYNAKÇA
8. EKLER

**ŞEKİLLER DİZİNİ**

- Şekil 1: TikTok İçerik Üreticisi Seçimi ve Optimizasyonu Genel İş Akış Şeması
- Şekil 2: Takipçi Sayısı vs. Beğeni Sayısı İlişkisi
- Şekil 3: Video Süresi vs. Beğeni Sayısı
- Şekil 4: Takipçi Sayısı vs. İçerik Üreticisi Skoru

**TABLOLAR DİZİNİ**

- Tablo 5.1. Takipçi Bazlı Kademeli Maliyet Modeli
- Tablo 5.2. Kategori Maliyet Çarpanları
- Tablo 5.3. MCDM Kriter Ağırlık Tablosu
- Tablo 5.4. Gurobi Çözücü Parametre Tablosu
- Tablo E.1. İş-Zaman Çizelgesi
- Tablo E.2. Risk Yönetim Tablosu (B Planı)

---

## 1. GİRİŞ

Dijitalleşmenin hız kazanmasıyla birlikte pazarlama faaliyetleri önemli ölçüde dönüşmüş, markalar hedef kitlelerine ulaşmak için sosyal medya platformlarını daha yoğun biçimde kullanmaya başlamıştır. Özellikle kısa video temelli içeriklerin yaygınlaşması, kullanıcıların içerik tüketim alışkanlıklarını değiştirmiş ve markalar açısından yeni iletişim olanakları yaratmıştır. Bu bağlamda TikTok, algoritmik keşif yapısı ve yüksek etkileşim oranları sayesinde dijital pazarlama stratejilerinde öne çıkan platformlardan biri hâline gelmiştir.

TikTok üzerinde yürütülen marka iş birliklerinde içerik üreticileri, yalnızca tanıtım yapan kişiler olarak değil, marka algısını şekillendiren önemli paydaşlar olarak değerlendirilmektedir. Ancak uygulamada içerik üreticisi seçimi çoğu zaman takipçi sayısı, toplam beğeni miktarı veya önceki iş birliklerine ilişkin genel izlenimlere dayalı olarak yapılmaktadır. Bu tür yaklaşımlar, içerik üreticisinin hedef kitleyle olan uyumunu ve gerçek etkileşim performansını yeterince yansıtmayabilmektedir.

ENM457 (Bitirme Projesi I) kapsamında gerçekleştirilen ilk aşamada, TikTok platformundan içerik üreticilerine ait veri seti web kazıma yöntemleri ile elde edilmiş ve bu veriler ön incelemeye tabi tutulmuştur. Bu süreçte elde edilen veri altyapısı, çalışmanın ikinci aşaması için zemin oluşturmuştur.

ENM458 (Bitirme Projesi II) kapsamındaki bu raporda ise, elde edilen veri seti ileri düzey analizler için dönüştürülmüş, içerik üreticisi seçimine yönelik çok kriterli değerlendirme modeli oluşturulmuş ve 0-1 Tam Sayılı Doğrusal Programlama (ILP) yöntemiyle optimal influencer portföyü belirlenmektedir. Geliştirilen sistem, Streamlit tabanlı bir karar destek arayüzüyle son kullanıcıya sunulmakta; teknik bilgisi olmayan pazarlama yöneticilerinin bile saniyeler içinde optimize edilmiş influencer önerisi almasını mümkün kılmaktadır.

Bu rapor, ENM458 dersi 1. ile 6. haftalar arasındaki çalışmaları (Ara Sınav Raporu) kapsamakta olup modelin dayandığı yöntemi, veri hazırlık sürecini ve gerçekleştirilen uygulamayı bütünleşik biçimde aktarmaktadır.

---

## 2. PROBLEMİN TARİFİ

Bu çalışma, dijital pazarlama alanında TikTok platformu üzerinde gerçekleştirilen marka–içerik üreticisi iş birliklerine odaklanmaktadır. TikTok, kısa video formatı ve yüksek etkileşim yapısı sayesinde markaların geniş kitlelere ulaşmasını mümkün kılmakta, bu durum içerik üreticisi seçiminin stratejik önemini artırmaktadır.

Çalışmanın temel problemi, TikTok üzerinde gerçekleştirilecek marka iş birlikleri için uygun içerik üreticilerinin nasıl belirleneceğidir. Mevcut uygulamalarda bu süreç çoğunlukla takipçi sayısı veya öznel değerlendirmelere dayandırılmakta; video bazlı etkileşim yapıları ve içerik performansı yeterince dikkate alınmamaktadır. Bu durum, özellikle sınırlı bütçeye sahip kampanyalarda reklam kaynaklarının verimsiz kullanılmasına yol açmaktadır.

TikTok'un algoritmik yapısı, içerik üreticisi performansının yalnızca basit göstergelerle açıklanmasını zorlaştırmaktadır. Yüksek takipçi sayısı her zaman yüksek etki anlamına gelmemekte; etkileşim oranı, içerik türü ve kullanıcı davranışları daha belirleyici hâle gelmektedir. Bu nedenle içerik üreticisi seçiminin çok boyutlu performans göstergeleri ile ele alınması gerekmektedir.

Problemin önemli bir teknik boyutu, Türkiye'de TikTok verilerine doğrudan erişim sağlayan bir API bulunmamasıdır. Bu durum, veri temelli analizleri zorlaştırmakta ve alternatif veri toplama yöntemlerini gerekli kılmaktadır.

Bu çalışma kapsamında problem iki aşamalı olarak ele alınmaktadır:

**İlk Aşama (ENM457):** İçerik üreticilerine ait veriler web kazıma yöntemiyle toplanmış, veri seti temizlenmiş ve yalnızca Türkiye'de faaliyet gösteren bireysel içerik üreticileri analize dahil edilmiştir.

**İkinci Aşama (ENM458):** Veri seti analitik dönüşümden geçirilmiş; etkileşim vekili, maliyet tahmini ve MCDM skoru hesaplanmıştır. Ardından belirli bir bütçe altında en yüksek etkiyi sağlayacak içerik üreticisi kombinasyonunu seçen bir 0-1 ILP optimizasyon modeli geliştirilmiş ve Streamlit arayüzüyle bütünleştirilmiştir.

Problemin gerçekçi kısıtları şunlardır: Ekonomik açıdan reklam bütçesi sınırlıdır ve her influencer'ın tahmini maliyeti farklıdır; stratejik açıdan marka, belirli kategorilerde mutlaka temsilci istemektedir; itibar yönetimi açısından bazı influencer'larla çalışılmak istenmemektedir (kara liste); risk yönetimi açısından ise tüm bütçenin tek bir hesaba ayrılması hem finansal hem de PR riski taşımaktadır.

---

## 3. LİTERATÜR TARAMASI

Bu bölümde, çalışmanın konusunu oluşturan içerik üreticisi pazarlaması, içerik üreticisi performansının değerlendirilmesi, veri temelli ve hesaplamalı yaklaşımlar ile bütçe kısıtlı karar verme modelleri literatürdeki çalışmalar çerçevesinde ele alınmaktadır. İncelenen çalışmalar, içerik üreticisi seçiminin hangi kriterler doğrultusunda yapıldığını ortaya koymakta ve bu tez çalışmasının literatürde konumlandığı noktayı belirlemektedir.

Dijital içerik üreticisi kavramı, sosyal medya platformlarının yaygınlaşmasıyla birlikte pazarlama literatüründe önemli bir yer edinmiştir. Johnson ve Alvarez, dijital içerik üreticilerinin markalar ile tüketiciler arasında güven temelli bir köprü kurduğunu ve geleneksel reklamcılıktan farklı bir etkileşim yapısı sunduğunu belirtmektedir [1]. Benzer şekilde Kumar ve Lee, içerik üreticisi pazarlamasını sosyal platformların doğasıyla birlikte ele alarak, bu pazarlama biçiminin kullanıcı etkileşimi ve içerik özgünlüğü üzerine kurulu olduğunu vurgulamıştır [2].

Zhang ve Han tarafından gerçekleştirilen çalışmada, influencer pazarlamasının teorik temelleri, güncel eğilimleri ve gelecekteki araştırma yönleri kapsamlı biçimde incelenmektedir; çalışmada 2023 itibarıyla sektör hacminin 21 milyar doları aştığı ve içerik üreticisi seçiminin giderek daha analitik bir yapıya kavuştuğu ifade edilmektedir [3]. Andersson ve Bergström ise ampirik bulgularla, influencer başarısının yalnızca takipçi sayısıyla ölçülemeyeceğini; içerik kalitesi ve etkileşim yapısının da belirleyici olduğunu ortaya koymuştur [4].

Son yıllarda içerik üreticisi pazarlamasında hesaplamalı yöntemlerin kullanımı artış göstermiştir. Li ve Wang, büyük veri analitiği ve ağ tabanlı yöntemlerin içerik üreticisi etkinliğini anlamada önemli katkılar sunduğunu belirtmiştir [5]. Araujo, Neijens ve Vliegenthart ise etkili içerik üreticilerinin keşfedilmesinde ağ yapıları ve etkileşim örüntülerinin kritik rol oynadığını ortaya koymuştur [6].

Saito ve Kobayashi tarafından geliştirilen SI modeli, içerik üreticisi maksimizasyon problemini matematiksel bir çerçevede ele alarak, sosyal medya yayılımının analitik olarak modellenebileceğini göstermektedir [7]. Tiukhova, Korovin ve Melnikov tarafından önerilen dinamik grafik sinir ağları tabanlı yaklaşım ise içerik üreticisi tahminini zaman boyutunu da kapsayacak biçimde ele almış; statik değil dinamik değerlendirmenin önemini vurgulamıştır [8].

İçerik üreticisi pazarlamasında bütçe, karar verme sürecini doğrudan etkileyen temel unsurlardan biridir. Influencer Marketing Benchmark Report 2023, markaların influencer pazarlamasına ayırdığı bütçelerin arttığını, ancak bu bütçelerin etkin kullanımına yönelik analitik yaklaşımların hâlâ sınırlı olduğunu ortaya koymaktadır [9]. Kim ve Cho, bütçe kısıtları altında optimal influencer kampanyasının nasıl oluşturulabileceğini incelemiş ve veri temelli planlamanın kampanya başarısını anlamlı biçimde artırdığını göstermiştir [10]. López-Dawn ve Giovanidis ise içerik üreticisi seçimini bütçe kısıtlı bir portföy optimizasyon problemi olarak ele alarak sistematik bir çözüm önermiştir [11].

De Veirman, Cauberghe ve Hudders, yüksek takipçi sayısının her zaman daha yüksek etki anlamına gelmediğini ve güven algısıyla doğrusal olmayan bir ilişki içinde olduğunu göstermiştir [12]. Lou ve Yuan ise influencer mesajlarının algılanan değeri ve güvenilirliğinin tüketici güvenini doğrudan etkilediğini belirtmiştir [13]. Phua, Jin ve Kim tarafından gerçekleştirilen çalışmada, parasosyal etkileşimin kullanıcı davranışları üzerindeki belirleyici rolü ortaya konmuştur [14]. Bu bulguların tamamı, etkileşim kalitesini, güven algısını ve içerik özelliklerini çok boyutlu bir değerlendirme çerçevesinde ele almanın zorunluluğunu desteklemektedir.

Dijital ve sosyal medya pazarlamasında geleceğe yönelik araştırma yönlerini inceleyen Dwivedi ve arkadaşları, bu tür karar problemlerinde hesaplamalı yöntemler, büyük veri analitiği ve karar destek modellerinin belirleyici rol oynayacağını vurgulamaktadır [15]. Mevcut tez çalışması, literatürde önerilen bu yönelimle tam uyum içinde biçimde, içerik üreticisi seçimini veri temelli ve optimizasyon odaklı bir çerçevede ele almaktadır.

### 3.1. Genel Değerlendirme ve Tezin Literatürdeki Konumu

Literatür incelendiğinde, içerik üreticisi pazarlamasının kavramsal temellerinin büyük ölçüde oluşturulduğu, ancak platforma özgü ve veri temelli çalışmaların hâlâ sınırlı olduğu görülmektedir. Özellikle TikTok gibi algoritmik keşif yapısına sahip platformlar için geliştirilen içerik üreticisi seçim yaklaşımları oldukça kısıtlıdır. Mevcut çalışmalar büyük çoğunlukla Instagram veya YouTube gibi platformlarda yoğunlaşmakta; Türkiye ölçeğindeki TikTok dinamiklerini yansıtmamaktadır.

Bu tez çalışması; TikTok özelinde gerçek platform verilerine dayalı veri toplama, çok kriterli skorlama ve 0-1 ILP optimizasyonunun bir arada kullanıldığı bütünleşik bir sistem sunarak literatürdeki önemli bir boşluğu doldurmaktadır. Çalışma, hem kuramsal hem de uygulamaya yönelik katkı sağlamayı amaçlamaktadır: kuramsal katkı, TikTok influencer seçiminin matematiksel bir optimizasyon problemi olarak modellenmesiyle; uygulamaya yönelik katkı ise Streamlit arayüzü ile doğrudan kullanılabilir bir karar destek sistemi sunulmasıyla gerçekleştirilmektedir.

---

## 4. PROJENİN GİRİŞİMCİLİK VE YENİLİKÇİLİK AÇISINDAN KATKISI

Bu çalışma, dijital pazarlama alanında giderek artan influencer kullanımına rağmen influencer seçim sürecinin büyük ölçüde sezgisel ve deneyime dayalı biçimde yürütülmesine yönelik bir problemi ele almaktadır. Özellikle küçük ve orta ölçekli işletmeler açısından yanlış influencer tercihlerinin reklam bütçeleri üzerinde önemli kayıplara yol açabildiği görülmektedir. Bu bağlamda çalışma, influencer seçimini veri temelli ve analitik bir yaklaşımla ele alarak girişimcilik açısından uygulanabilir bir çözüm sunmayı hedeflemektedir.

Girişimcilik perspektifinden değerlendirildiğinde, geliştirilen Streamlit arayüzü aylık abonelik modeliyle (B2B SaaS) dijital ajanslar ve markalara sunulabilecek, minimum uygulanabilir ürün (MVP) niteliğinde bir altyapı oluşturmaktadır. TikTok'a özgü verilerin sistematik biçimde toplanması, temizlenmesi, analiz edilmesi ve matematiksel modele entegre edilmesiyle ortaya çıkan bu sistem; influencer seçim sürecinin ölçülebilir, karşılaştırılabilir ve optimize edilebilir hâle getirilmesine olanak tanımaktadır.

Yenilikçilik açısından çalışmanın öne çıkan boyutları şunlardır: Türkiye'de TikTok verisine dayalı influencer seçimi için geliştirilen ilk optimizasyon modeli olma özelliği; API erişimi gerektirmeyen, web kazıma tabanlı özgün veri toplama altyapısı; takipçi sayısı yerine etkileşim kalitesini merkeze alan MCDM skorlama sistemi; gerçek zamanlı senaryo simülasyonu (farklı bütçe, kategori ve kara liste kombinasyonları); teknik bilgi gerektirmeyen sezgisel kullanıcı arayüzü. Proje aynı zamanda Endüstri Mühendisliği (optimizasyon modeli), Bilgisayar Mühendisliği (web kazıma, Streamlit) ve İşletme (pazarlama stratejisi, maliyet modeli) disiplinlerini başarıyla entegre eden multidisipliner bir yapıya sahiptir.

Geliştirilen yaklaşım, ilerleyen aşamalarda ticarileştirilebilir bir karar destek sistemine dönüştürülebilecek potansiyel taşımaktadır. Bu yönüyle proje, salt bir akademik çalışmanın ötesine geçerek yazılımsal katma değer üreten bir mühendislik girişim prototipi sergilemektedir.

### 4.1. Projenin BM Sürdürülebilir Kalkınma Amaçları Kapsamında Topluma, Ekonomiye, Sürdürülebilirliğe ve Çevreye Etkileri

Bu çalışma, Birleşmiş Milletler Sürdürülebilir Kalkınma Amaçları (SKA) kapsamında iki temel hedefle doğrudan ilişkilendirilmektedir.

**SKA 8 — İnsana Yakışır İş ve Ekonomik Büyüme:** Dijital reklam dünyasındaki mevcut yapıda, harcamaların büyük bölümü Mega (1 milyondan fazla takipçili) içerik üreticilerinde yoğunlaşmaktadır. Bu durum, organik etkileşim oranları yüksek ancak henüz geniş kitlelere ulaşamamış Nano (0–10 bin takipçi) ve Micro (10 bin–100 bin takipçi) düzeydeki yaratıcıların ekosistemin dışında kalmasına neden olmaktadır. Geliştirilen optimizasyon modeli, maliyet etkinliği kriterini sisteme dahil ederek bu dengesizliği düzeltmektedir. Yüksek etkileşim kalitesine sahip küçük ölçekli içerik üreticileri çok boyutlu değerlendirmeden geçirildiğinde algoritma tarafından öne çıkarılabilmekte; KOBİ'ler ve yerel markalar da uygun maliyetli ama etkili işbirliği yapma imkânı bulmaktadır.

**SKA 12 — Sorumlu Üretim ve Tüketim:** Sezgisel kararlarla tahsis edilen reklam bütçeleri kaynak israfına ve başarısız kampanyaların tekrarlanmasına yol açmaktadır. Her başarısız kampanya hem finansal kayıp hem de gereksiz dijital içerik üretimi (dolayısıyla enerji tüketimi) anlamına gelmektedir. Bu proje, her harcanan reklam lirasının matematiksel hesap görmeyi zorunlu kılan bir sistem kurarak sorumlu tüketimi teşvik etmekte ve dijital reklam sektöründe sürdürülebilir bir karar verme kültürünün yerleşmesine katkı sağlamaktadır.

Toplumsal açıdan değerlendirildiğinde, daha hedefli içerik üretiminin teşvik edilmesi, kullanıcıların ilgisiz ve tekrarlayan reklamlara maruz kalmasını azaltarak dijital içerik tüketiminde daha dengeli bir yapı oluşturulmaktadır. Ekonomik açıdan ise reklam bütçelerinin veri temelli kararlarla yönetilmesi, yatırım geri dönüşünü artırarak özellikle sınırlı kaynaklara sahip işletmeler için rekabet avantajı yaratmaktadır.

---

## 5. ÇALIŞMADA KULLANILAN TEMEL KAVRAMLAR VE YÖNTEMLER

Sosyal medya üzerinde yürütülen influencer pazarlama faaliyetlerinin etkinliği, içerik üreticilerine ait güvenilir, tutarlı ve çok boyutlu verilerin sistematik biçimde analiz edilebilmesine bağlıdır. Takipçi sayısı, etkileşim oranı, video başına beğeni ortalaması ve içerik üretim sıklığı gibi nicel göstergeler; içerik üreticilerinin marka açısından yaratacağı potansiyel etkiyi ölçmede belirleyici rol oynamaktadır.

Ancak TikTok platformu, Türkiye özelinde resmi bir API sunmamaktadır. Bu durum, tüm veri toplama sürecini teknik ve operasyonel açıdan çalışmanın en kritik aşamalarından biri hâline getirmektedir. Bu çalışmada benimsenen metodolojik çerçeve şu aşamaları kapsamaktadır:

*[Şekil 1: TikTok İçerik Üreticisi Seçimi ve Optimizasyonu Genel İş Akış Şeması]*

### 5.1. Veri Toplama Süreci ve Ön İşleme

İçerik üreticilerine ait veriler, Python programlama dili kullanılarak geliştirilen Selenium tabanlı dinamik web kazıma yöntemiyle elde edilmiştir. Veri toplama sürecine başlanmadan önce, analiz edilecek içerik üreticileri için bir başlangıç örneklemi oluşturulmuş; birden fazla kez yer alan kullanıcı adları temizlenmiş, kurumsal ya da marka hesapları ile içerik üreticisi pazarlaması kapsamında değerlendirilemeyecek profiller elenmiştir.

Kazıma süreci kapsamında her içerik üreticisi için profil sayfasına erişilerek şu veriler toplanmıştır: kullanıcı adı, görünen ad, biyografi bilgisi, takipçi sayısı, takip edilen hesap sayısı, toplam beğeni sayısı, video sayısı; video sayfalarından ise görüntülenme sayısı, beğeni, yorum ve paylaşım sayıları ile içerik kategorisi bilgileri. TikTok'un doğrulama mekanizmaları devreye girdiğinde, etik ve teknik sınırlar gözetilerek otomatik aşma yöntemleri kullanılmamış; manuel müdahale sonrası süreç kaldığı yerden sürdürülmüştür.

Veri kalitesini artırmak amacıyla kapsamlı bir ön işleme ve temizleme süreci gerçekleştirilmiştir. Veriler; veri temizleme, filtreleme ve yalnızca Türkiye'de faaliyet gösteren bireysel içerik üreticileri seçilerek yapılandırılmış tablolar hâline getirilmiştir.

**Keşifsel Analizler:**

Toplanan veriler üzerinde gerçekleştirilen keşifsel analiz kapsamında, içerik üreticilerinin takipçi sayıları ile video başına elde ettikleri beğeni sayıları arasındaki ilişki incelenmiştir. Elde edilen sonuçlar, takipçi sayısının artmasının her durumda doğrusal etkileşim artışıyla sonuçlanmadığını ortaya koymaktadır.

*[Şekil 2: Takipçi Sayısı vs. Beğeni Sayısı İlişkisi]*

Video süresi ile beğeni sayısı arasındaki ilişki logaritmik ölçekte analiz edilmiş; farklı video sürelerine sahip içeriklerin benzer düzeylerde etkileşim elde edebildiği gözlemlenmiştir. Bu bulgu, kullanıcı etkileşiminin video süresinden ziyade içerik niteliği ve etkileşim dinamikleriyle daha yakından ilişkili olduğunu göstermektedir.

*[Şekil 3: Video Süresi vs. Beğeni Sayısı]*

Çok boyutlu performans skoru ile takipçi sayısı arasındaki ilişki analiz edildiğinde, yüksek takipçi sayısının her zaman yüksek performans skoruna karşılık gelmediği görülmüştür. Bu durum, seçim sürecinde yalnızca takipçi sayısına dayanan yaklaşımların yetersiz kaldığını göstermektedir.

*[Şekil 4: Takipçi Sayısı vs. İçerik Üreticisi Skoru]*

### 5.2. Analitik Dönüşüm Adımları

Ham veri doğrudan optimizasyon modeline aktarılamaz. ENM458 kapsamında toplanan veriler üç aşamalı bir analitik dönüşüm sürecinden geçirilmiştir.

**5.2.1. Etkileşim Vekili (Engagement Proxy) Hesaplanması**

Yalnızca takipçi sayısına dayalı değerlendirmeler yanıltıcı olabilmektedir. Bu nedenle her içerik üreticisi için iki bileşenli bir Etkileşim Vekili skoru türetilmiştir:

- **Bileşen 1 — Takipçi Başına Beğeni Oranı:** like_per_follower = avg_video_likes / max(followers, 1)
- **Bileşen 2 — Ortalama Video Beğeni Logaritması:** log_avg_likes = ln(1 + avg_video_likes)
- **Etkileşim Vekili (Normalize Edilmiş):** Engagement_Proxy = 0.60 × MinMax(like_per_follower) + 0.40 × MinMax(log_avg_likes)

%60 ağırlık, organik sadık kitleye sahip küçük üreticilerin adaletli biçimde temsil edilmesini sağlarken; %40 ağırlık, mutlak büyüklük avantajını değerlendirmeye katmaktadır.

**5.2.2. Tahmini Maliyet Modeli (Cost Estimation Model)**

TikTok işbirliği ücretleri kamuya açık değildir. Sektör benchmarkları ve uzman görüşlerine dayanan kademeli (tier-based) bir maliyet modeli geliştirilmiştir. Temel maliyet formülü: Maliyet = (Taban Ücret + Takipçi/1000 × Artış Oranı) × Kategori Çarpanı.

**Tablo 5.1. Takipçi Bazlı Kademeli Maliyet Modeli**

| Kademe (Tier) | Takipçi Aralığı | Taban Ücret | Artış Oranı (TL / 1K takipçi) |
|---------------|-----------------|-------------|-------------------------------|
| Nano          | 0 – 10.000      | 1.500 TL    | 150 TL |
| Micro         | 10.000 – 100.000 | 8.000 TL  | 80 TL  |
| Mid           | 100.000 – 500.000 | 35.000 TL | 35 TL  |
| Macro         | 500.000 – 1.000.000 | 90.000 TL | 20 TL |
| Mega          | 1.000.000+      | 200.000 TL  | 8 TL   |

**Tablo 5.2. Kategori Maliyet Çarpanları**

| Kategori | Çarpan |
|----------|--------|
| Beauty & Personal Care (Güzellik ve Bakım) | 1.15 |
| Fashion & Style (Moda ve Stil) | 1.10 |
| Technology & Digital (Teknoloji) | 1.05 |
| Travel & Lifestyle (Seyahat) | 1.05 |
| Fitness & Health (Spor ve Sağlık) | 1.00 |
| Music & Performance (Müzik) | 1.00 |
| Mixed/Unclear | 1.00 |
| Food & Cooking (Yemek) | 0.95 |
| Comedy & Entertainment (Komedi) | 0.90 |
| Gaming (Oyun) | 0.90 |
| Education & Informative (Eğitim) | 0.85 |

**5.2.3. Çok Kriterli Karar Verme (MCDM) Skoru**

Birden fazla kriterin bütünleşik biçimde değerlendirilmesi için ağırlıklı doğrusal birleştirme yöntemi kullanılmıştır. Her kriter önce Min-Max normalizasyonuyla [0, 1] aralığına çekilmiş; ardından belirlenen ağırlıklarla ağırlıklı toplamı alınmıştır.

**Tablo 5.3. MCDM Kriter Ağırlık Tablosu**

| Kriter | Açıklama | Ağırlık |
|--------|----------|---------|
| Etkileşim Skoru | Engagement Proxy | %35 |
| Takipçi Büyüklüğü | log(1 + followers) | %20 |
| Takipçi Başına Beğeni | like_per_follower | %20 |
| Maliyet Etkinliği | log(avg_likes) / tahmini maliyet | %15 |
| Video Hacmi | Video üretim sayısı | %10 |

Formül: MCDM_Score = 0.35 × c1 + 0.20 × c2 + 0.20 × c3 + 0.15 × c4 + 0.10 × c5

Bu ağırlık yapısının tasarım mantığı şudur: etkileşim kalitesi (%55 birleşik ağırlıkla) en güçlü belirleyici unsur iken takipçi sayısının yalnızca büyüklüğü tek başına yeterli kabul edilmemektedir. Maliyet etkinliği (%15) bütçe kullanımını optimize ederken, video hacmi (%10) aktif içerik üretimini ödüllendirmektedir.

### 5.3. Optimizasyon Modeli: 0-1 Tam Sayılı Doğrusal Programlama

MCDM skorları ve maliyet tahminleri hesaplandıktan sonra, influencer seçim problemi 0-1 Tam Sayılı Doğrusal Programlama (ILP) modeli olarak kurulmuştur. ILP, karar değişkenlerinin tamsayı (0 veya 1) değerler almasını zorunlu kılan doğrusal optimizasyon modelidir. Influencer seçimi doğası gereği ikili bir karar yapısına sahiptir: bir influencer ya seçilir ya da seçilmez. Kim ve Cho [10] ile López-Dawn ve Giovanidis [11], benzer yapıdaki influencer seçim problemlerini matematiksel programlama yöntemiyle çözmenin kampanya etkinliğini anlamlı biçimde artırdığını göstermiştir.

**Karar Değişkeni:**
- xᵢ ∈ {0, 1}, ∀i ∈ {1, 2, …, n}
- xᵢ = 1 → i. içerik üreticisi portföye dahil edilir; xᵢ = 0 → seçilmez

**Amaç Fonksiyonu (Maksimizasyon):**
- Z = Σ MCDM_Scoreᵢ × xᵢ

**Kısıt 1 — Bütçe Kısıtı:** Σ costᵢ × xᵢ ≤ B (Hedef kampanya bütçesi)

**Kısıt 2 — Minimum Çeşitlilik:** Σ xᵢ ≥ n_min (Risk dağıtımı için en az n_min influencer seçimi)

**Kısıt 3 — Maksimum Portföy Büyüklüğü (İsteğe Bağlı):** Σ xᵢ ≤ n_max

**Kısıt 4 — Tier Bazlı Üst Sınır:** Belirli kademedeki influencer sayısı sınırlandırılarak risk dengesi yönetilir

**Kısıt 5 — Zorunlu Kategori Temsili:** Seçilen kategorilerde en az bir influencer bulunması sağlanır

**Kısıt 6 — Kara Liste (Blacklist):** xₖ = 0, ∀k ∈ K_black (Kara listedeki influencer'lar kesinlikle seçilmez)

Model, Gurobi Solver (gurobipy Python kütüphanesi) ile çözülmektedir. Gurobi, Dal-ve-sınır (Branch-and-Bound) algoritması temelinde çalışan, akademik ve ticari kullanımda geniş bir kullanım alanına sahip matematiksel programlama çözücüsüdür.

**Tablo 5.4. Gurobi Çözücü Parametre Tablosu**

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| TimeLimit | 60 saniye | Maksimum çözüm süresi |
| MIPGap | 0.001 | %0.1 optimallik toleransı |
| Threads | 4 | Paralel iş parçacığı sayısı |
| MIPFocus | 1 | İyi çözüm bulmaya odaklan |
| Presolve | 2 | Agresif ön-çözme |

Model, optimal çözüme ulaştığında (Optimal), zaman limitinde çözüm bulduğunda (TimeLimit) veya uygulanabilir çözüm bulamadığında (Infeasible) ya da bütçe yetersiz kaldığında kullanıcıya bilgi vermektedir.

Model çıktıları incelendiğinde, farklı bütçe seviyelerinde seçilen içerik üreticilerinin dağılımının değiştiği gözlemlenmiştir. Özellikle düşük bütçelerde daha yüksek etkileşim oranına sahip Micro influencer'ların tercih edildiği, bütçe arttıkça daha geniş erişim sağlayan influencer'ların da seçime dahil edildiği belirlenmiştir.

### 5.4. Streamlit Tabanlı Karar Destek Arayüzü

Yalnızca konsol çıktılarından ibaret akademik projeler ticari hayatta hızla geride kalmaktadır. Bu açığı kapatmak için Streamlit framework'ü kullanılarak dinamik bir karar destek web uygulaması (streamlit_app.py) oluşturulmuştur.

Arayüz özellikleri şöyle sıralanabilir:

- **Bütçe Slaydırı:** Kampanya bütçesi 1.000 TL ile 10.000.000 TL arasında dinamik olarak belirlenebilir
- **Kategori Seçimi:** Zorunlu içerik kategorileri çoklu seçim kutucuklarıyla tanımlanabilir
- **Kara Liste Yönetimi:** İstenmeyen influencer'lar listeden seçilerek otomatik olarak model dışında tutulur; profil görselleri de görüntülenir
- **Optimizasyon Tetikleyicisi:** Tek tuşa basılarak Gurobi modeli arka planda çalıştırılır
- **Sonuç Görüntüleme:** Seçilen influencer sayısı, kullanılan bütçe, kalan bütçe ve toplam MCDM skoru metrik kartlarda gösterilir; seçilen influencer'lar ızgara düzeninde fotoğrafları, kategorileri, takipçi sayıları, tahmini maliyetleri ve MCDM skorlarıyla listelenir

Bu arayüz tasarımı, teknik bilgiden bağımsız olarak bir pazarlama yöneticisinin modeli doğrudan kullanabilmesini sağlamaktadır.

---

## 6. SONUÇ VE ÖNERİLER

Bu tez çalışmasının ENM458 kapsamındaki ilk altı haftasında gerçekleştirilen çalışmalar ve ulaşılan sonuçlar şu şekilde özetlenebilir.

Birinci dönemde (ENM457), Selenium tabanlı web kazıma yöntemiyle oluşturulan TikTok veri seti ikinci dönemde (ENM458) analitik dönüşüm süreçlerinden geçirilerek optimizasyon modeline hazır hale getirilmiştir. Etkileşim vekili hesaplamaları, takipçi sayısının tek başına performansı açıklamadaki yetersizliğini bir kez daha doğrulamıştır; yüksek takipçili bazı hesapların, düşük takipçili ama etkileşim odaklı hesapların gerisinde MCDM skoru aldığı gözlemlenmiştir.

Gurobi ILP modeli, farklı bütçe senaryolarında (50K, 150K, 300K, 600K TL) tutarlı ve matematiksel olarak optimal portföyler üretmektedir. Model, geleneksel sezgisel yaklaşımların aksine portföy bütçesini katmanlar arasında dengeleyerek hem maliyet etkinliğini hem de kategori çeşitliliğini optimize etmektedir. Streamlit arayüzü, modeli teknik bilgisi bulunmayan son kullanıcılara başarıyla sunmaktadır.

**Sınırlılıklar:** Maliyet modeli, gerçek piyasa fiyatlarının sektör benchmarklarına dayanan bir tahminini temsil etmekte; bireysel pazarlık koşulları yansıtılmamaktadır. Veri seti yalnızca belirli bir zaman dilimini kapsamakta olup influencer performansı zaman içinde dalgalanabilmektedir. Web kazıma yöntemi yalnızca herkese açık profillerle sınırlıdır.

**Çalışmanın mevcut aşamasındaki önemli bir not:** Birinci dönem raporunda (ENM457), "herhangi bir optimizasyon veya çok kriterli karar verme modeli uygulanmamıştır" olarak belirtilen olgu, ENM458 kapsamında tamamıyla aşılmış; MCDM skorlama ve Gurobi ILP modeli başarıyla hayata geçirilmiş ve Streamlit arayüzüne entegre edilmiştir.

**Sonraki Aşamada Planlanlar (Hafta 7–14):**

- Farklı bütçe seviyeleri ve kriter ağırlık kombinasyonları için kapsamlı duyarlılık analizi (Sensitivity Analysis) gerçekleştirilecektir
- Modelin farklı marka profilleri (KOBİ, büyük ölçekli marka) için örnek vaka çalışmaları hazırlanacaktır
- Streamlit arayüzüne senaryo karşılaştırma ve sonuç dışa aktarma (Excel/PDF) özellikleri eklenecektir
- Tüm çalışma ENM458 tez yazım kılavuzuna uygun biçimde formatlanarak nihai form hâline taşınacaktır

Sonuç olarak bu çalışma, TikTok platformu özelinde içerik üreticisi pazarlamasına yönelik veri temelli bir optimizasyon sistemi sunarak içerik üreticisi seçiminin daha bilinçli, ölçülebilir ve sistematik biçimde gerçekleştirilmesine katkı sağlamaktadır. Geliştirilen yöntemsel ve yazılımsal altyapı hem akademik literatüre hem de dijital pazarlama uygulamalarına yönelik önemli bir temel oluşturmakta; ilerleyen çalışmalar için genişletilebilir ve uyarlanabilir bir çerçeve sunmaktadır.

---

## KAYNAKÇA

[1] Johnson, M., & Alvarez, L. (2021). *The Rise of Digital Influencers: Shaping the Future of Marketing*. Journal of Digital Communication, 14(3), 210–225.

[2] Kumar, R., & Lee, D. (2020). *Influencer Marketing with Social Platforms*. Social Media Research Journal, 8(4), 112–130.

[3] Zhang, P., & Han, Y. (2023). *Social Media Influencer Marketing: Foundations, Trends and Research Directions*. International Journal of Marketing Science, 19(1), 55–74.

[4] Andersson, S., & Bergström, E. (2020). *Instagram and Influencer Marketing: An Empirical Study of the Parameters Behind Success*. Procedia Economics and Business, 7(2), 89–101.

[5] Li, C., & Wang, H. (2022). *Computational Studies in Influencer Marketing*. Expert Systems with Applications, 193, 116–127.

[6] Araujo, T., Neijens, P., & Vliegenthart, R. (2019). *Discovering Effective Influencers*. Computers in Human Behavior, 98, 10–20.

[7] Saito, M., & Kobayashi, K. (2019). *A SI Model for Social Media Influencer Maximization*. IEEE Access, 7, 150876–150889.

[8] Tiukhova, L., Korovin, D., & Melnikov, P. (2022). *Influencer Prediction with Dynamic Graph Neural Networks*. Neural Networks, 154, 145–159.

[9] Influencer Marketing Hub. (2023). *Influencer Marketing Benchmark Report 2023*. Global Industry Review Series.

[10] Kim, S., & Cho, Y. (2023). *Optimal Influencer Marketing Campaign under Budget Constraints*. Journal of Business Analytics, 12(3), 180–195.

[11] López-Dawn, A., & Giovanidis, A. (2021). *Budgeted Portfolio Optimization Model for Social Media Influencer Selection*. Journal of Applied Optimization, 18(4), 300–315.

[12] De Veirman, M., Cauberghe, V., & Hudders, L. (2017). *Marketing through Instagram influencers: The impact of number of followers and product divergence*. International Journal of Advertising, 36(5), 798–828.

[13] Lou, C., & Yuan, S. (2019). *Influencer marketing: How message value and credibility affect consumer trust*. Journal of Interactive Advertising, 19(1), 58–73.

[14] Phua, J., Jin, S. V., & Kim, J. (2020). *The roles of celebrity endorsers' credibility and attractiveness in influencer marketing*. Computers in Human Behavior, 102, 310–321.

[15] Dwivedi, Y. K., et al. (2021). *Setting the future of digital and social media marketing research*. International Journal of Information Management, 59, 102168.

---

## 7. EKLER

### Tablo E.1. İş-Zaman Çizelgesi

| No | İş Paketlerinin Adı | Zaman Aralığı (Ay) | Takım Lideri | Ekip Üyeleri |
|----|---------------------|--------------------|--------------|--------------| 
| 1 | Veri Toplama Stratejisinin Belirlenmesi ve Ön Analiz | Ekim – Kasım 2025 | Esra Zeyrek | Abdullah Raif Yıldırım, Oğuzhan Dikmen |
| 2 | Kapsamlı Verinin Toplanması ve Veri Temizleme Süreci | Kasım – Aralık 2025 | Abdullah Raif Yıldırım | Esra Zeyrek, Oğuzhan Dikmen |
| 3 | Toplanan Verilerin İşlenmesi ve İstatistiksel Değerlendirme | Aralık 2025 – Ocak 2026 | Oğuzhan Dikmen | Abdullah Raif Yıldırım, Esra Zeyrek |
| 4 | Engagement Proxy, MCDM Skoru ve Maliyet Modeli Geliştirme | Ocak – Şubat 2026 | Abdullah Raif Yıldırım | Esra Zeyrek, Oğuzhan Dikmen |
| 5 | ILP Modelinin Kurulması, Gurobi Entegrasyonu ve Streamlit Arayüzü | Şubat – Mart 2026 | Esra Zeyrek | Abdullah Raif Yıldırım, Oğuzhan Dikmen |
| 6 | Model Çözümü, Test Süreci ve Duyarlılık Analizi | Nisan – Mayıs 2026 | Oğuzhan Dikmen | Abdullah Raif Yıldırım, Esra Zeyrek |
| 7 | Sonuçların Değerlendirilmesi ve Raporlama | Mayıs 2026 | Esra Zeyrek | Abdullah Raif Yıldırım, Oğuzhan Dikmen |

### Tablo E.2. Risk Yönetim Tablosu (B Planı)

| No | En Büyük Riskler | Risk Yönetimi (B Planı) |
|----|-----------------|------------------------|
| 1 | TikTok platformunun veri erişimini kısıtlaması veya doğrulama mekanizmalarını artırması | İnsan davranışını taklit eden esnek scraper yapısı kullanılmaktadır. Kısıtlama artarsa veri çekme hızı azaltılacak, mevcut veri seti ek kaynaklarla zenginleştirilecektir. |
| 2 | Toplanan verinin analiz için yetersiz kalması | Başlangıç örneklemi genişletilebilir biçimde tasarlanmıştır. Veri yetersizliğinde kullanıcı sayısı artırılacak veya normalize metrikler kullanılacaktır. |
| 3 | API eksikliği nedeniyle veri tutarlılığının sağlanamaması | Veriler yalnızca herkese açık kaynaklardan toplanmış, veri temizleme ve çapraz doğrulama ile tutarlılık güvence altına alınmıştır. |
| 4 | Web kazıma sürecinde teknik hatalar veya kesintiler yaşanması | Ara kayıt (checkpoint) mekanizmalarıyla veri kaybı önlenmiştir. Hata durumunda süreç kaldığı yerden devam eder. |
| 5 | Optimizasyon modelinde uygulanabilir çözüm bulunamaması (infeasible) | Bütçe artırılacak, kategori kısıtları esnetilecek veya kara liste daraltılacaktır. Arayüz bu durumda kullanıcıya öneride bulunmaktadır. |
| 6 | Gurobi lisans sorunları yaşanması | PuLP + CBC (açık kaynak) çözücüsüne geçiş B planı olarak hazır tutulmaktadır. Model bu geçişe uyumlu biçimde kodlanmıştır. |
| 7 | Zaman planına uyulamaması | İş paketleri paralel planlanmıştır. Gecikme durumunda kapsam daraltılarak temel model tutulacak, gelişmiş özellikler sonraki versiyona aktarılacaktır. |
