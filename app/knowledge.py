# Navtera bilgi tabani: chatbotun yatlar ve lokasyonlar hakkinda bildigi her sey burada.
# Yeni yat eklemek / bilgi guncellemek icin sadece bu dosyayi duzenlemek yeterli.

YACHTS = [
    {
        "ad": "Riva Rivamare 38",
        "tip": "Ahşap runabout geleneğinden gelen lüks motoryat",
        "uzunluk": "11.88 m",
        "gunduz_kapasite": 8,
        "konaklama_kapasite": 2,
        "motor": "Çift Volvo Penta D6-400 hp",
        "maks_hiz": "40 knot",
        "tanitim": (
            "Markanın efsanevi ahşap runabout geleneğini modern teknoloji ve kusursuz İtalyan "
            "işçiliğiyle buluşturan büyüleyici bir sanat eseri. Hız tutkusunu konforla harmanlar."
        ),
    },
    {
        "ad": "Sanlorenzo SX76",
        "tip": "Crossover süperyat (filonun amiral gemilerinden)",
        "uzunluk": "23.75 m",
        "gunduz_kapasite": 12,
        "konaklama_kapasite": 8,
        "motor": "Çift Volvo Penta D13-IPS1350 (1000 hp)",
        "maks_hiz": "22 knot",
        "tanitim": (
            "Lüksü ve mühendislik harikası tasarımı bir arada sunan üstün bir crossover süperyat. "
            "Geniş yaşam alanlarıyla uzun blue tour seyahatleri için kusursuz konfor; "
            "huzurlu ve prestijli bir seyir deneyimi."
        ),
    },
    {
        "ad": "Frauscher 1414 Demon",
        "tip": "Yüksek performanslı lüks spor motoryat",
        "uzunluk": "13.92 m",
        "gunduz_kapasite": 10,
        "konaklama_kapasite": 4,
        "motor": "Çift Volvo Penta D6-440 DPI",
        "maks_hiz": "48 knot",
        "tanitim": (
            "Keskin hatları, fütüristik sportif çizgileri ve nefes kesen performansıyla adrenalin "
            "tutkunları için tasarlandı. Dalgalara meydan okuyan dinamik bir sürüş deneyimi."
        ),
    },
    {
        "ad": "VanDutch 48",
        "tip": "Minimalist tasarımlı üst segment motoryat",
        "uzunluk": "14.60 m",
        "gunduz_kapasite": 12,
        "konaklama_kapasite": 2,
        "motor": "Çift Volvo Penta IPS650 (2 x 480 hp)",
        "maks_hiz": "36 knot",
        "tanitim": (
            "Minimalist ve ikonik tasarımıyla denizde bakışları üzerine çeken, modern lüksün ve "
            "prestijin simgesi. 2 kişilik kabiniyle özel seyahatler için ideal; güçlü ve son derece "
            "dengeli bir seyir performansı."
        ),
    },
    {
        "ad": "Pardo 43",
        "tip": "Walkaround yat",
        "uzunluk": "14.00 m",
        "gunduz_kapasite": 12,
        "konaklama_kapasite": 4,
        "motor": "Çift Volvo Penta IPS600 (435 hp)",
        "maks_hiz": "35 knot",
        "tanitim": (
            "Yürüyüş yolları, geniş güneşlenme alanları ve üstün İtalyan tasarımıyla açık deniz "
            "konforunu en üst seviyeye taşır. Hidrodinamik gövde yapısıyla benzersiz bir sürüş keyfi."
        ),
    },
    {
        "ad": "Wallytender 43",
        "tip": "Yenilikçi tasarımlı tender / motoryat",
        "uzunluk": "13.20 m",
        "gunduz_kapasite": 10,
        "konaklama_kapasite": 2,
        "motor": "Çift Volvo Penta V8-430 hp",
        "maks_hiz": "40 knot",
        "tanitim": (
            "Radikal ve yenilikçi tasarımı, genişletilebilir güverte alanları ve üst düzey denizcilik "
            "özellikleriyle çığır açan bir model. Sportif çeviklik ile modern estetik bir arada."
        ),
    },
    {
        "ad": "Solaris Power 48 Open",
        "tip": "Open yat",
        "uzunluk": "14.35 m",
        "gunduz_kapasite": 12,
        "konaklama_kapasite": 4,
        "motor": "Çift Volvo Penta IPS650",
        "maks_hiz": "35 knot",
        "tanitim": (
            "Klasik denizci çizgilerini modern lüksle harmanlayan, denge ve dalga kesme performansıyla "
            "öne çıkan bir open yat. En sert sularda bile sarsıntısız ve güvenli seyir."
        ),
    },
    {
        "ad": "Chris-Craft Corsair 34",
        "tip": "Klasik Amerikan runabout",
        "uzunluk": "10.36 m",
        "gunduz_kapasite": 10,
        "konaklama_kapasite": 2,
        "motor": "Çift Mercury V8 8.2L (2 x 430 hp)",
        "maks_hiz": "42 knot",
        "tanitim": (
            "Klasik Amerikan runabout ruhunu zarafet ve nostaljik detaylarla buluşturan zamansız bir "
            "lüks klasik. Nostaljik estetik ve heyecan verici performans bir arada."
        ),
    },
    {
        "ad": "Sunseeker Hawk 38",
        "tip": "Yarış DNA'lı spor tekne (filonun en hızlısı)",
        "uzunluk": "11.85 m",
        "gunduz_kapasite": 6,
        "konaklama_kapasite": 2,
        "motor": "Çift Mercury Racing 400R / 450R",
        "maks_hiz": "60+ knot",
        "tanitim": (
            "Tamamen hız, performans ve yarış DNA'sı üzerine kurulmuş, adeta su üstünde uçan agresif "
            "ve sofistike bir spor tekne. Filonun en hızlı ve adrenalin dolu deneyimi."
        ),
    },
    {
        "ad": "Azimut Grande 27M",
        "tip": "Süperyat (filonun taç mücevheri)",
        "uzunluk": "26.78 m",
        "gunduz_kapasite": 12,
        "konaklama_kapasite": 10,
        "motor": "Çift MAN V12 (1900 hp)",
        "maks_hiz": "28 knot",
        "tanitim": (
            "Karbon fiber mimarisi ve muazzam iç hacmiyle üstün konforlu bir süperyat. 10 kişilik "
            "konaklamasıyla lüks otel konforunu denize taşır; hem menzil hem üst düzey prestij."
        ),
    },
    {
        "ad": "Anvera 48",
        "tip": "Tamamen karbon fiber yüksek performans yat",
        "uzunluk": "14.50 m",
        "gunduz_kapasite": 12,
        "konaklama_kapasite": 2,
        "motor": "Çift Mercury 627 hp",
        "maks_hiz": "50 knot",
        "tanitim": (
            "Tamamen karbon fiberden üretilen fütüristik gövdesi, devasa güneşlenme terası ve hafiflik "
            "mimarisiyle denizcilik dünyasının geleceğini yansıtır. Hız ve estetik zirvede."
        ),
    },
]

LOCATIONS = [
    {
        "ad": "İstanbul",
        "ozet": (
            "Boğaziçi'nde, iki kıta arasında, tarihi yalılar ve saraylar eşliğinde şehir manzaralı "
            "bir yat deneyimi. Günübirlik turlar, gün batımı turları, doğum günü / evlilik teklifi "
            "gibi özel organizasyonlar için ideal."
        ),
        "one_cikanlar": [
            "Boğaz turu: Dolmabahçe ve Çırağan sarayları, Ortaköy Camii, Boğaziçi Köprüsü",
            "Bebek, Arnavutköy, Kuruçeşme sahilleri ve tarihi yalılar",
            "Rumeli Hisarı ve Anadolu Hisarı",
            "Kız Kulesi",
            "Prens Adaları (Adalar) açıkları",
        ],
        "sezon": "Yıl boyu yapılabilir; en keyifli dönem ilkbahar, yaz ve sonbahar. Gün batımı turları çok popüler.",
    },
    {
        "ad": "Bodrum",
        "ozet": (
            "Ege'nin en popüler lüks tatil merkezi. Turkuaz koylar, şık beach club'lar ve canlı gece "
            "hayatı. Günübirlik koy turlarından birkaç günlük mavi tura kadar her şeye uygun."
        ),
        "one_cikanlar": [
            "Bodrum Kalesi manzarası",
            "Yalıkavak Marina ve çevresi",
            "Türkbükü ve Göltürkbükü",
            "Gümüşlük (gün batımı ve balık restoranları)",
            "Karaada (doğal sıcak su mağarası)",
            "Orak Adası ve berrak koyları",
        ],
        "sezon": "Ana sezon mayıs - ekim arası; temmuz ve ağustos en yoğun dönem.",
    },
    {
        "ad": "Göcek",
        "ozet": (
            "Akdeniz'in çam ormanlarıyla çevrili, sakin ve korunaklı koylarıyla meşhur mavi tur "
            "cenneti. Huzur, doğa ve demirleyip yüzmek isteyenler için ideal; Dalaman Havalimanı'na yakın."
        ),
        "one_cikanlar": [
            "12 Adalar turu",
            "Yassıca Adaları (sığ turkuaz su)",
            "Tersane Adası",
            "Bedri Rahmi Koyu",
            "Kızılada",
            "Sarsala Koyu ve Boynuz Bükü",
        ],
        "sezon": "Ana sezon mayıs - ekim arası; deniz haziran - eylül arasında en sıcak.",
    },
]


def build_knowledge_text():
    """Bilgi tabanini AI'nin okuyacagi duz metne cevirir."""
    lines = ["## NAVTERA FİLOSU"]
    for i, y in enumerate(YACHTS, 1):
        lines.append(
            f"\n### {i}. {y['ad']}\n"
            f"- Tip: {y['tip']}\n"
            f"- Uzunluk: {y['uzunluk']}\n"
            f"- Gündüz misafir kapasitesi: {y['gunduz_kapasite']} kişi\n"
            f"- Konaklama kapasitesi: {y['konaklama_kapasite']} kişi\n"
            f"- Motor: {y['motor']}\n"
            f"- Maksimum hız: {y['maks_hiz']}\n"
            f"- Tanıtım: {y['tanitim']}"
        )

    lines.append("\n## HİZMET VERDİĞİMİZ LOKASYONLAR")
    for loc in LOCATIONS:
        lines.append(f"\n### {loc['ad']}\n{loc['ozet']}\nÖne çıkanlar:")
        lines.extend(f"- {item}" for item in loc["one_cikanlar"])
        lines.append(f"Sezon: {loc['sezon']}")

    return "\n".join(lines)
