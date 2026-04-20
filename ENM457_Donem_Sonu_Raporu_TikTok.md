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
**Ocak, 2026**

---

## ÖZET

**TİKTOK'TA ETKİLİ MARKA İŞ BİRLİĞİ İÇİN İÇERİK ÜRETİCİSİ SEÇİMİNİN OPTİMİZASYONU**

**Esra ZEYREK | Abdullah Raif YILDIRIM | Oğuzhan DİKMEN**

Endüstri Mühendisliği  
Eskişehir Teknik Üniversitesi, Mühendislik Fakültesi, Ocak, 2026  
Danışman: Asst. Prof. Dr. Zeliha ERGÜL AYDIN

Dijital pazarlama faaliyetlerinin sosyal medya platformlarına kaymasıyla birlikte, içerik üreticileri markalar için önemli bir iletişim aracı hâline gelmiştir. Özellikle TikTok, kısa video formatı ve yüksek etkileşim oranları sayesinde marka iş birliklerinin yoğunlaştığı bir platform olarak öne çıkmaktadır. Ancak içerik üreticisi (influencer) seçimi çoğu zaman takipçi sayısı gibi sınırlı göstergelere dayandırılmakta, bu durum reklam bütçelerinin etkin kullanılmasını zorlaştırmaktadır.

Bu çalışma, TikTok üzerinde gerçekleştirilecek marka iş birlikleri için veri temelli bir içerik üreticisinin seçim sürecinin altyapısının oluşturulmasını amaçlamaktadır. Türkiye'de TikTok API erişiminin kısıtlı olması nedeniyle, içerik üreticilerinin ait veriler Selenium tabanlı web kazıma yöntemiyle toplanmıştır. Geliştirilen veri toplama süreci kapsamında, içerik üreticilerinin profil bilgileri ile video bazlı etkileşim metrikleri sistematik biçimde elde edilmiştir. Doğrulama gerektiren durumlarda manuel müdahale ile sürecin devam ettirilmesi sağlanmıştır.

Toplanan veriler, içerik üreticilerinin performanslarını yansıtabilecek göstergelerin oluşturulması amacıyla ön incelemeye tabi tutulmuştur. Elde edilen veri setinin, çalışmanın ikinci döneminde geliştirilecek olan optimizasyon temelli karar modeline girdi oluşturması planlanmaktadır. Bu yönüyle çalışma, içerik üreticisi seçim sürecinin sezgisel yaklaşımlardan uzaklaştırılarak daha ölçülebilir ve sistematik bir yapıya kavuşturulmasına katkı sağlamaktadır. Ayrıca çalışma, dijital reklam kaynaklarının daha bilinçli kullanılmasını hedeflemesi bakımından Birleşmiş Milletler Sürdürülebilir Kalkınma Amaçlarından SKA 12: Sorumlu Üretim ve Tüketim ile ilişkilidir.

**Anahtar Sözcükler:** TikTok, içerik üreticisi seçimi, web kazıma, dijital pazarlama, etkileşim metrikleri, veri temelli karar verme, sorumlu tüketim

---

## ABSTRACT

**OPTIMIZATION OF CONTENT CREATOR SELECTION FOR EFFECTIVE BRAND COLLABORATIONS ON TIKTOK**

**Esra ZEYREK | Abdullah Raif YILDIRIM | Oğuzhan DİKMEN**

Department of Industrial Engineering  
Eskisehir Technical University, Engineering Faculty, January, 2026  
Supervisor: Asst. Prof. Dr. Zeliha ERGÜL AYDIN

With the shift of marketing activities toward social media platforms, content creators have become a key component of brand communication strategies. In particular, TikTok has emerged as a prominent platform for brand collaborations due to its short-video format and high user engagement. However, the selection of content creators is often based on limited indicators such as follower count, which may lead to inefficient use of advertising budgets.

This study aims to establish a data-driven foundation for the content creator selection process in TikTok-based brand collaborations. Due to the limited accessibility of TikTok's API in Türkiye, data related to content creators were collected using a Selenium-based web scraping approach. Within this process, profile information and video-level engagement metrics were systematically obtained. In cases requiring verification, the data collection process was continued through manual intervention.

The collected data were subjected to preliminary analysis to derive performance-related indicators for content creators. The resulting dataset is intended to serve as an input for an optimization-based decision model to be developed in the second phase of the study. In this respect, the study contributes to transforming the content creator selection process from intuitive practices into a more structured and measurable framework. Furthermore, by promoting more efficient use of digital advertising resources, the study is associated with Sustainable Development Goal 12: Responsible Consumption and Production.

**Keywords:** TikTok, content creator selection, web scraping, digital marketing, engagement metrics, data-driven decision making, responsible consumption

---

## İÇİNDEKİLER

1. [GİRİŞ](#1-giriş)
2. [PROBLEMİN TARİFİ](#2-problemin-tarifi)
3. [LİTERATÜR TARAMASI](#3-literatür-taraması)
   - 3.1. Genel Değerlendirme ve Tezin Literatürdeki Konumu
4. [PROJENİN GİRİŞİMCİLİK VE YENİLİKÇİLİK AÇISINDAN KATKISI](#4-projenin-girişimcilik-ve-yenilikçilik-açısından-katkısı)
   - 4.1. Projenin BM Sürdürülebilir Kalkınma Amaçları Kapsamında Etkileri
5. [ÇALIŞMADA KULLANILAN TEMEL KAVRAMLAR VE YÖNTEMLER](#5-çalışmada-kullanılan-temel-kavramlar-ve-yöntemler)
6. [SONUÇ VE ÖNERİLER](#6-sonuç-ve-öneriler)
- [KAYNAKÇA](#kaynakça)
7. [EKLER](#7-ekler)

**Şekiller Dizini:**
- Şekil 1: TikTok İçerik Üreticisi Seçimi ve Optimizasyonu Genel İş Akış Şeması
- Şekil 2: Takipçi Sayısı vs. Beğeni Sayısı İlişkisi
- Şekil 3: Video Süresi vs. Beğeni Sayısı
- Şekil 4: Takipçi Sayısı vs. İçerik Üreticisi Skoru

**Tablolar Dizini:**
- Tablo 1: E.1. İş-Zaman Çizelgesi
- Tablo 2: E.2. Risk Yönetim Tablosu (B Planı)

---

## 1. GİRİŞ

Dijitalleşmenin hız kazanmasıyla birlikte pazarlama faaliyetleri önemli ölçüde dönüşmüş, markalar hedef kitlelerine ulaşmak için sosyal medya platformlarını daha yoğun biçimde kullanmaya başlamıştır. Özellikle kısa video temelli içeriklerin yaygınlaşması, kullanıcıların içerik tüketim alışkanlıklarını değiştirmiş ve markalar açısından yeni iletişim olanakları yaratmıştır. Bu bağlamda TikTok, algoritmik keşif yapısı ve yüksek etkileşim oranları sayesinde dijital pazarlama stratejilerinde öne çıkan platformlardan biri hâline gelmiştir.

TikTok üzerinde yürütülen marka iş birliklerinde içerik üreticileri (içerik üreticisi), yalnızca tanıtım yapan kişiler olarak değil, marka algısını şekillendiren önemli paydaşlar olarak değerlendirilmektedir. Ancak uygulamada içerik üreticisi seçimi çoğu zaman takipçi sayısı, toplam beğeni miktarı veya önceki iş birliklerine ilişkin genel izlenimlere dayalı olarak yapılmaktadır. Bu tür yaklaşımlar, içerik üreticisinin hedef kitleyle olan uyumunu ve gerçek etkileşim performansını yeterince yansıtmayabilmektedir.

Özellikle sınırlı bütçeye sahip markalar için yanlış içerik üreticisi tercihi, reklam kaynaklarının verimsiz kullanılmasına yol açabilmektedir. Bu durum hem beklenen etkileşimin sağlanamamasına hem de dijital reklam harcamalarının sürdürülebilir olmayan bir yapıya bürünmesine neden olmaktadır. Bu nedenle içerik üreticisi seçimi, yalnızca pazarlama odaklı bir karar olarak değil; birden fazla kriterin ve kısıtın dikkate alınmasını gerektiren bir karar verme problemi olarak ele alınmalıdır.

Bu çalışma, TikTok üzerinde gerçekleştirilecek marka iş birlikleri için veri temelli bir içerik üreticisi seçim sürecinin altyapısının oluşturulmasını amaçlamaktadır. Çalışmanın bu aşamasında odak noktası, içerik üreticilerine ait güvenilir ve sistematik bir veri setinin elde edilmesidir. Türkiye'de TikTok API erişiminin kısıtlı olması nedeniyle veri toplama süreci web kazıma yöntemleriyle yürütülmüş ve elde edilen veriler ön incelemeye tabi tutulmuştur.

Bu proje, Türkiye'de TikTok verisine dayalı geliştirilecek ilk içerik üreticisi optimizasyon modeli olma özelliğini taşımaktadır. Modelin özgünlüğü, yalnızca belirli parametrelerle sınırlı kalmaması; markaların kendi dinamiklerine göre tanımlanabilen esnek kriterleri içermesinden kaynaklanmaktadır.

---

## 2. PROBLEMİN TARİFİ

Bu çalışma, dijital pazarlama alanında TikTok platformu üzerinde gerçekleştirilen marka–içerik üreticisi iş birliklerine odaklanmaktadır. TikTok, kısa video formatı sayesinde içeriklerin hızlı biçimde yayılmasına olanak tanımakta ve kullanıcı etkileşimini ön plana çıkarmaktadır.

Çalışmanın temel problemi, TikTok üzerinde gerçekleştirilecek marka iş birlikleri için uygun içerik üreticilerinin nasıl belirleneceğidir. Mevcut uygulamalarda bu süreç çoğu zaman sınırlı sayıda göstergeye dayandırılmakta; içerik üreticilerinin video bazlı etkileşim yapıları ve içerik performansları ayrıntılı biçimde analiz edilmemektedir. Uygulamada içerik üreticisi seçimi genellikle takipçi sayısı, önceki kampanya deneyimleri veya öznel değerlendirmelere dayalı olarak yapılmaktadır.

TikTok'un algoritmik keşif yapısı ve içerik yayılım mekanizması, içerik üreticisi performansının yalnızca takipçi sayısı gibi basit göstergelerle açıklanmasını zorlaştırmaktadır. Bir içerik üreticisinin yüksek takipçi sayısına sahip olması, kampanya başarısını garanti etmemekte; video bazlı etkileşim oranları, içerik türü ve kullanıcı etkileşimi gibi faktörler çok daha belirleyici hâle gelmektedir.

Problemin bir diğer önemli boyutu, Türkiye'de TikTok verilerine doğrudan erişim sağlayan resmî bir uygulama programlama arayüzünün (API) bulunmamasıdır. Bu durum, TikTok üzerinde gerçekleştirilecek veri temelli analizleri teknik açıdan zorlaştırmakta ve araştırmacıları alternatif veri toplama yöntemlerine yönlendirmektedir.

Bu bağlamda problem, yalnızca hangi içerik üreticilerinin seçileceği değil; bu seçimin hangi verilere dayanarak ve hangi yöntemlerle yapılacağıdır. Bu çalışma kapsamında ele alınan problem, iki aşamalı bir yapı içerisinde incelenmektedir:

1. **İlk aşama:** TikTok platformundan içerik üreticilerine ait profil ve video bazlı etkileşim verilerinin web kazıma yöntemiyle toplanması ve bu verilerden performans göstergelerinin elde edilmesi.
2. **İkinci aşama:** Oluşturulan veri seti kullanılarak içerik üreticisi seçimine yönelik analitik ve optimizasyon temelli bir karar modelinin geliştirilmesi.

Bu tez çalışması, özellikle ilk aşamaya odaklanarak, ikinci aşama için gerekli olan veri temelli altyapının oluşturulmasını amaçlamaktadır.

---

## 3. LİTERATÜR TARAMASI

Bu bölümde, çalışmanın konusunu oluşturan içerik üreticisi pazarlaması, içerik üreticisi performansının değerlendirilmesi, veri temelli ve hesaplamalı yaklaşımlar ile bütçe kısıtlı karar verme modelleri literatürdeki çalışmalar çerçevesinde ele alınmaktadır.

Johnson ve Alvarez, dijital içerik üreticilerinin markalar ile tüketiciler arasında güven temelli bir köprü kurduğunu ve geleneksel reklamcılıktan farklı bir etkileşim yapısı sunduğunu belirtmektedir [1]. Benzer şekilde Kumar ve Lee, içerik üreticisi pazarlamasını sosyal platformların doğasıyla birlikte ele alarak, bu pazarlama biçiminin kullanıcı etkileşimi ve içerik özgünlüğü üzerine kurulu olduğunu vurgulamıştır [2].

Zhang ve Han tarafından gerçekleştirilen çalışmada, içerik üreticisi pazarlamasının teorik temelleri, güncel eğilimleri ve gelecekteki araştırma yönleri kapsamlı biçimde incelenmiştir [3]. İçerik üreticisi başarısının ölçülmesinde sıklıkla takipçi sayısı, beğeni ve yorum miktarı gibi nicel göstergeler kullanılmaktadır. Ancak Andersson ve Bergström tarafından yapılan ampirik çalışmada, içerik üreticisi başarısının yalnızca bu göstergelere indirgenemeyeceği, içerik kalitesi ve etkileşim yapısının da belirleyici olduğu ortaya konmuştur [4].

Son yıllarda içerik üreticisi pazarlamasında hesaplamalı yöntemlerin kullanımı artış göstermiştir. Li ve Wang, içerik üreticisi pazarlamasına yönelik hesaplamalı çalışmaları inceleyerek, büyük veri analitiği ve ağ tabanlı yöntemlerin içerik üreticisi etkinliğini anlamada önemli katkılar sunduğunu belirtmiştir [5]. Saito ve Kobayashi tarafından geliştirilen SI modeli, içerik üreticisi maksimizasyon problemini matematiksel bir çerçevede ele alarak, sosyal medya yayılımının analitik olarak modellenebileceğini göstermektedir [7].

Tiukhova, Korovin ve Melnikov tarafından önerilen dinamik grafik sinir ağları tabanlı yaklaşım ise içerik üreticisi tahminini zaman boyutunu da dikkate alarak ele almıştır [8]. Kim ve Cho, bütçe kısıtları altında optimal içerik üreticisi kampanyasının nasıl oluşturulabileceğini incelemiş ve veri temelli planlamanın kampanya başarısını artırdığını göstermiştir [10]. López-Dawn ve Giovanidis ise içerik üreticisi seçimini bütçe kısıtlı bir portföy optimizasyon problemi olarak ele almış ve en uygun içerik üreticisi kombinasyonunun belirlenmesine yönelik bir model önermiştir [11].

De Veirman, Cauberghe ve Hudders, yüksek takipçi sayısının her zaman daha yüksek etki anlamına gelmediğini göstermiştir [12]. Lou ve Yuan ise içerik üreticisi mesajlarının algılanan değeri ve güvenilirliğinin tüketici güvenini doğrudan etkilediğini belirtmiştir [13].

### 3.1. Genel Değerlendirme ve Tezin Literatürdeki Konumu

Literatür incelendiğinde, içerik üreticisi pazarlamasının kavramsal temellerinin büyük ölçüde oluşturulduğu, ancak platforma özgü ve veri temelli çalışmaların hâlâ sınırlı olduğu görülmektedir. Özellikle TikTok gibi algoritmik keşif yapısına sahip platformlar için geliştirilen içerik üreticisi seçim yaklaşımları oldukça kısıtlıdır.

Bu tez çalışması, içerik üreticisi pazarlamasını TikTok özelinde, gerçek platform verilerine dayalı ve veri temelli bir karar problemi olarak ele alması bakımından literatürdeki önemli bir boşluğu hedeflemektedir. Web kazıma yöntemiyle elde edilen veriler üzerinden içerik üreticisi performansının analiz edilmesi, çalışmayı mevcut yaklaşımlardan ayırmaktadır.

---

## 4. PROJENİN GİRİŞİMCİLİK VE YENİLİKÇİLİK AÇISINDAN KATKISI

Bu çalışma, dijital pazarlama alanında giderek artan içerik üreticisi kullanımına rağmen, içerik üreticisi seçim sürecinin çoğunlukla sezgisel ve deneyime dayalı biçimde yürütülmesine yönelik bir probleme odaklanmaktadır. Özellikle küçük ve orta ölçekli işletmeler açısından, yanlış içerik üreticisi tercihlerinin reklam bütçeleri üzerinde önemli kayıplara yol açabildiği görülmektedir.

Girişimcilik perspektifinden değerlendirildiğinde, bu tez kapsamında geliştirilen yaklaşım; dijital pazarlama ajansları, markalar ve bireysel girişimler tarafından kullanılabilecek bir karar destek altyapısının temelini oluşturmaktadır. TikTok platformuna özgü verilerin sistematik biçimde toplanması ve analiz edilmesi, içerik üreticisi seçim sürecinin daha ölçülebilir ve şeffaf hâle getirilmesine olanak tanımaktadır.

Yenilikçilik açısından çalışmanın öne çıkan yönlerinden biri, Türkiye'de TikTok API erişiminin sınırlı olması nedeniyle veri toplama sürecinin web kazıma yöntemiyle gerçekleştirilmesidir. Geliştirilen veri toplama yapısı, login gerektirmeden çalışabilen ve doğrulama gerektiren durumlarda manuel müdahale sonrası süreci sürdürebilen esnek bir yaklaşım sunmaktadır.

Ayrıca, içerik üreticisi pazarlamasının çoğunlukla tekil metrikler üzerinden değerlendirildiği mevcut uygulamalardan farklı olarak, bu çalışma çok boyutlu performans göstergelerinin oluşturulmasına odaklanmaktadır. Elde edilen veri setinin, çalışmanın ilerleyen aşamalarında optimizasyon temelli karar modellerine girdi olarak kullanılabilecek olması, yenilikçi ve ölçeklenebilir bir yapı sunmaktadır.

### 4.1. Projenin BM Sürdürülebilir Kalkınma Amaçları Kapsamında Topluma, Ekonomiye, Sürdürülebilirliğe ve Çevreye Etkileri

Bu çalışma, Birleşmiş Milletler Sürdürülebilir Kalkınma Amaçları (SKA) arasında yer alan **SKA 12: Sorumlu Üretim ve Tüketim** ile doğrudan ilişkilidir.

**Toplumsal açıdan:** Bu çalışma kapsamında geliştirilen veri temelli yaklaşım, kullanıcıların maruz kaldığı içeriklerin daha hedefli ve anlamlı hâle gelmesine katkı sağlamaktadır. İçerik üreticisi seçim sürecinin daha bilinçli biçimde yürütülmesi, kullanıcıların tekrarlayan ve ilgisiz reklamlara maruz kalmasını azaltarak dijital ortamda daha dengeli bir içerik tüketim yapısının oluşmasına yardımcı olmaktadır.

**Ekonomik açıdan:** İçerik üreticisi seçim sürecinin sistematik hâle getirilmesi, özellikle sınırlı bütçeyle çalışan işletmeler ve girişimler için önemli avantajlar sunmaktadır. Reklam bütçelerinin veri temelli kararlarla yönetilmesi, başarısız kampanya riskini azaltmakta ve pazarlama yatırımlarının geri dönüşünü artırmaktadır.

**Sürdürülebilirlik ve çevre açısından:** Dijital reklamcılık faaliyetlerinin plansız biçimde artırılması, gereksiz içerik üretimi ve yüksek işlem gücü gerektiren dijital altyapıların daha yoğun kullanılmasına yol açabilmektedir. Bu çalışma kapsamında oluşturulan yaklaşım, içerik üreticisi pazarlamasında daha hedefli ve ölçülebilir kararlar alınmasını destekleyerek dolaylı enerji tüketiminin azaltılmasına katkı sunmaktadır.

---

## 5. ÇALIŞMADA KULLANILAN TEMEL KAVRAMLAR VE YÖNTEMLER

Sosyal medya platformları üzerinde yürütülen içerik üreticisi pazarlama (influencer marketing) faaliyetlerinin etkinliği, büyük ölçüde içerik üreticilerine ait güvenilir, tutarlı ve çok boyutlu verilerin sistematik biçimde analiz edilebilmesine bağlıdır. Takipçi sayısı, etkileşim oranı, izlenme performansı ve içerik üretim sıklığı gibi nicel göstergeler; içerik üreticilerinin markalar açısından yaratabileceği potansiyel etkiyi ölçmede temel rol oynamaktadır.

Ancak TikTok platformu, veri erişimi ve şeffaflık açısından diğer sosyal medya platformlarına kıyasla daha sınırlayıcı bir yapıya sahiptir. Türkiye özelinde TikTok'un resmî bir uygulama programlama arayüzü (API) sunmaması; içerik üreticilerine ait profil bilgileri, video performans metrikleri ve etkileşim verilerinin doğrudan, yapılandırılmış ve otomatik bir biçimde elde edilmesini mümkün kılmamaktadır.

Bu çalışma kapsamında geliştirilen metodolojik çerçeve:

- TikTok içerik üreticilerine ait çok boyutlu performans verilerinin dinamik web kazıma teknikleriyle elde edilmesi
- Elde edilen verilerin analitik olarak işlenmesi
- Nicel metriklere dayalı bir optimizasyon modeli aracılığıyla içerik üreticisi seçiminin sistematik hâle getirilmesi

amaçlarını kapsamaktadır.

**Veri Toplama Süreci:**

Çalışmada kullanılan veriler, içerik üreticilerinin herkese açık profil sayfalarından ve bu profillerde paylaşılan videolardan elde edilmiştir. Veri toplama süreci, Python programlama dili kullanılarak geliştirilen Selenium tabanlı bir web kazıma yaklaşımı ile yürütülmüştür.

Veri toplama sürecine başlanmadan önce, analiz edilecek içerik üreticilerinin belirlenmesi amacıyla bir başlangıç örneklem kümesi oluşturulmuştur. Oluşturulan başlangıç listesi üzerinde veri kalitesini artırmak amacıyla bir ön eleme süreci gerçekleştirilmiştir:
- Listede birden fazla kez yer alan kullanıcı adları temizlenmiştir.
- Bireysel içerik üreticisi niteliği taşımayan kurumsal veya marka hesapları ayıklanmıştır.
- İçerik üreticisi pazarlaması kapsamında değerlendirilemeyecek profiller çıkarılmıştır.

Veri toplama süreci, önceden belirlenmiş içerik üreticisi kullanıcı adlarının bir girdi dosyası üzerinden okunmasıyla başlatılmıştır. Her bir içerik üreticisi için profil sayfasına erişilerek kullanıcı adı, görünen ad, biyografi bilgisi, takipçi sayısı, takip edilen hesap sayısı ve toplam beğeni sayısı gibi temel profil verileri sistematik biçimde toplanmıştır. Video sayfalarına erişilerek görüntülenme sayısı, beğeni sayısı, yorum sayısı ve paylaşım sayısı gibi etkileşim metrikleri toplanmıştır.

TikTok platformu, belirli sayıda sayfa ziyareti sonrasında doğrulama (verify veya puzzle) mekanizmalarını devreye sokabilmektedir. Çalışma kapsamında etik ve teknik sınırlar gözetilerek otomatik doğrulama aşma yöntemleri kullanılmamıştır. Doğrulama ekranı ile karşılaşıldığında scraper bekleme moduna alınmış; doğrulama işlemi manuel olarak tamamlandıktan sonra veri toplama süreci kaldığı yerden devam etmiştir.

**Keşifsel Analizler:**

Toplanan veriler üzerinden yapılan keşifsel analiz kapsamında, içerik üreticilerinin takipçi sayıları ile video başına aldıkları beğeni sayıları arasındaki ilişki incelenmiştir. Elde edilen sonuçlar, takipçi sayısının artmasının her durumda etkileşim artışıyla sonuçlanmadığını göstermektedir.

Video içeriklerine ait özelliklerin kullanıcı etkileşimi üzerindeki etkisini değerlendirmek amacıyla video süresi ile beğeni sayısı arasındaki ilişki analiz edilmiştir. Logaritmik ölçekte gerçekleştirilen bu analiz, farklı video sürelerine sahip içeriklerin benzer düzeylerde etkileşim elde edebildiğini göstermektedir. Bu sonuç, kullanıcı etkileşiminin video süresinden ziyade içerik niteliği ve etkileşim dinamikleriyle daha yakından ilişkili olduğunu düşündürmektedir.

İçerik üreticilerinin çok boyutlu performanslarını temsil edebilmek amacıyla hesaplanan influencer skoru ile takipçi sayısı arasındaki ilişki ayrıca analiz edilmiştir. Elde edilen bulgular, yüksek takipçi sayısının her durumda yüksek performans skoruna karşılık gelmediğini ortaya koymaktadır. Bu durum, içerik üreticisi seçiminde yalnızca takipçi sayısına dayalı yaklaşımların yetersiz kaldığını göstermektedir.

---

## 6. SONUÇ VE ÖNERİLER

Bu tez çalışmasında, TikTok platformu üzerinde gerçekleştirilecek içerik üreticisi pazarlama faaliyetleri için veri temelli bir içerik üreticisi seçimi sürecinin altyapısı oluşturulmuştur. İçerik üreticisi seçiminin çoğu zaman sezgisel değerlendirmelere ve sınırlı metriklere dayalı olarak yapılması, pazarlama bütçelerinin etkin kullanımını zorlaştırmaktadır. Bu doğrultuda çalışma, içerik üreticisi seçimini analitik bir problem olarak ele almış ve bu problemin çözümü için gerekli olan veri toplama ve yapılandırma sürecine odaklanmıştır.

Çalışma kapsamında, Türkiye'de TikTok API erişiminin bulunmaması gibi önemli teknik kısıtlar altında, platformdan anlamlı ve analiz edilebilir verilerin elde edilebileceği gösterilmiştir. Selenium tabanlı web kazıma yöntemi kullanılarak geliştirilen veri toplama süreci sayesinde, içerik üreticilerine ait profil bilgileri ile video bazlı etkileşim metrikleri sistematik biçimde toplanmıştır.

Toplanan veriler üzerinde gerçekleştirilen keşifsel analizler, içerik üreticisi performansının yalnızca takipçi sayısı gibi tekil göstergelerle açıklanamayacağını ortaya koymuştur. Video bazlı görüntülenme, beğeni, yorum ve paylaşım sayıları gibi etkileşim metrikleri, içerik üreticilerinin hedef kitle ile kurduğu etkileşimi daha doğru biçimde yansıtmaktadır.

**Sınırlılıklar:**
- Veri toplama süreci, TikTok'un doğrulama mekanizmaları ve erişim kısıtları nedeniyle zaman zaman kesintiye uğramış ve manuel müdahale gerektiren durumlar ortaya çıkmıştır.
- Analizler yalnızca herkese açık profiller ve belirli sayıda içerik üreticisi ile sınırlı tutulmuştur.

**Gelecek Çalışmalar:**
- Bu tez kapsamında oluşturulan veri seti kullanılarak içerik üreticisi seçimine yönelik optimizasyon temelli karar modellerinin geliştirilmesi planlanmaktadır.
- Özellikle bütçe kısıtları altında en uygun içerik üreticilerinin belirlenmesi amacıyla çok kriterli karar verme ve matematiksel optimizasyon yöntemlerinin uygulanması öngörülmektedir.
- Analiz kapsamı genişletilerek farklı sektörlerdeki markalar ve farklı sosyal medya platformları için benzer yaklaşımlar geliştirilebilir.

Sonuç olarak bu tez çalışması, TikTok platformu özelinde içerik üreticisi pazarlamasına yönelik veri temelli bir yaklaşım sunarak, içerik üreticisi seçiminin daha bilinçli, ölçülebilir ve sistematik biçimde gerçekleştirilmesine katkı sağlamaktadır.

---

## KAYNAKÇA

[1] Johnson, M., & Alvarez, L. (2021). *The Rise of Digital Influencers: Shaping the Future of Marketing*. Journal of Digital Communication, 14(3), 210–225.

[2] Kumar, R., & Lee, D. (2020). *Influencer Marketing with Social Platforms*. Social Media Research Journal, 8(4), 112–130.

[3] Zhang, P., & Han, Y. (2023). *Social Media Influencer Marketing: Foundations, Trends and Research Directions*. International Journal of Marketing Science, 19(1), 55–74.

[4] Andersson, S., & Bergström, E. (2020). *Instagram and Influencer Marketing: An Empirical Study of the Parameters Behind Success*. Procedia Economics and Business, 7(2), 89–101.

[5] De Veirman, M., Cauberghe, V., & Hudders, L. (2017). *Marketing through Instagram influencers: The impact of number of followers and product divergence*. International Journal of Advertising, 36(5), 798–828.

[6] Lou, C., & Yuan, S. (2019). *Influencer marketing: How message value and credibility affect consumer trust*. Journal of Interactive Advertising, 19(1), 58–73.

[7] Phua, J., Jin, S. V., & Kim, J. (2020). *The roles of celebrity endorsers' credibility and attractiveness in influencer marketing*. Computers in Human Behavior, 102, 310–321.

[8] Li, C., & Wang, H. (2022). *Computational Studies in Influencer Marketing*. Expert Systems with Applications, 193, 116–127.

[9] Araujo, T., Neijens, P., & Vliegenthart, R. (2019). *Discovering Effective Influencers*. Computers in Human Behavior, 98, 10–20.

[10] Saito, M., & Kobayashi, K. (2019). *A SI Model for Social Media Influencer Maximization*. IEEE Access, 7, 150876–150889.

[11] Tiukhova, L., Korovin, D., & Melnikov, P. (2022). *Influencer Prediction with Dynamic Graph Neural Networks*. Neural Networks, 154, 145–159.

[12] Influencer Marketing Hub. (2023). *Influencer Marketing Benchmark Report 2023*. Global Industry Review Series.

[13] Kim, S., & Cho, Y. (2023). *Optimal Influencer Marketing Campaign under Budget Constraints*. Journal of Business Analytics, 12(3), 180–195.

[14] López-Dawn, A., & Giovanidis, A. (2021). *Budgeted Portfolio Optimization Model for Social Media Influencer Selection*. Journal of Applied Optimization, 18(4), 300–315.

[15] Dwivedi, Y. K., et al. (2021). *Setting the future of digital and social media marketing research*. International Journal of Information Management, 59, 102168.

---

## 7. EKLER

### Tablo E.1. İş-Zaman Çizelgesi

| No | İş Paketlerinin Adı | Zaman Aralığı | Takım Lideri | Ekip Üyeleri |
|----|---------------------|---------------|--------------|--------------|
| 1 | Veri Toplama Stratejisinin Belirlenmesi ve Ön Analiz | Ekim – Kasım 2025 | Esra Zeyrek | Abdullah Raif Yıldırım, Oğuzhan Dikmen |
| 2 | Kapsamlı Verinin Toplanması ve Veri Temizleme Süreci | Kasım – Aralık 2025 | Abdullah Raif Yıldırım | Esra Zeyrek, Oğuzhan Dikmen |
| 3 | Toplanan Verilerin İşlenmesi ve İstatistiksel Değerlendirme | Aralık 2025 – Ocak 2026 | Oğuzhan Dikmen | Abdullah Raif Yıldırım, Esra Zeyrek |
| 4 | Influencer Performans Analizi ve Tahmini Maliyet Fonksiyonunun Oluşturulması | Ocak 2026 | Abdullah Raif Yıldırım | Esra Zeyrek, Oğuzhan Dikmen |
| 5 | Matematiksel Modelin Kurulması ve Kodlanması (Tez II) | Şubat – Mart 2026 | Esra Zeyrek | Abdullah Raif Yıldırım, Oğuzhan Dikmen |
| 6 | Model Çözümü, Test Süreci ve Optimizasyon (Tez II) | Nisan – Mayıs 2026 | Oğuzhan Dikmen | Abdullah Raif Yıldırım, Esra Zeyrek |
| 7 | Sonuçların Değerlendirilmesi ve Raporlama | Mayıs 2026 | Esra Zeyrek | Abdullah Raif Yıldırım, Oğuzhan Dikmen |

### Tablo E.2. Risk Yönetim Tablosu (B Planı)

| No | En Büyük Riskler | Risk Yönetimi (B Planı) |
|----|------------------|-------------------------|
| 1 | TikTok platformunun veri erişimini kısıtlaması veya doğrulama mekanizmalarını artırması | İnsan davranışını taklit eden esnek scraper yapısı kullanılmıştır. Kısıtlama durumunda veri çekme hızı ve kapsamı azaltılarak sürecin devamı sağlanacaktır. |
| 2 | Toplanan verinin analiz için yetersiz kalması | Başlangıç örneklemi genişletilebilir şekilde tasarlanmıştır. Veri yetersizliğinde kullanıcı sayısı artırılacak veya normalize metrikler kullanılacaktır. |
| 3 | API eksikliği nedeniyle veri tutarlılığının sağlanamaması | Veriler yalnızca herkese açık kaynaklardan toplanmış, veri temizleme ve çapraz doğrulama ile tutarlılık sağlanmıştır. |
| 4 | Web kazıma sürecinde teknik hatalar veya kesintiler yaşanması | Ara kayıt mekanizmalarıyla veri kaybı önlenmiş, hata durumunda süreç kaldığı yerden devam edecek şekilde yapılandırılmıştır. |
| 5 | Optimizasyon modelinde veri uyumsuzluğu yaşanması | Veri seti tanımlı göstergelere göre düzenlenmiştir. Uyumsuzluk durumunda alternatif ölçütler ve normalize skorlar kullanılacaktır. |
| 6 | Zaman planına uyulamaması | İş paketleri paralel planlanmıştır. Gecikme durumunda kapsam daraltılarak modelleme süreci Tez II'ye aktarılacaktır. |
