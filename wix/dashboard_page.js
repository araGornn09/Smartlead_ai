// WIX SAYFA KODU — Dashboard sayfası > Sayfa Kodu: içindekileri tamamen sil, bunu yapıştır.
//
// Giriş için sayfada olması gereken elemanlar (ID'leri):
//   #sifreInput   → Metin girişi (şifre yazılacak kutu)
//   #girisButton  → Buton ("Giriş Yap")
//   #girisHata    → Metin (hata mesajı için, boş bırakılabilir)

import { getDashboardData } from 'backend/dashboard.web';

$w.onReady(function () {
    // Giriş yapılana kadar listeler gizli
    $w("#repeaterLeads").collapse();
    $w("#repeaterIletisim").collapse();
    $w("#girisHata").text = "";

    // ---------- REZERVASYONLAR ----------
    $w("#repeaterLeads").onItemReady(($item, itemData) => {
        $item("#txtIsim").text = itemData.isim || "İsim Bulunamadı";
        $item("#txtTelefon").text = itemData.telefon || "Telefon Bulunamadı";
        $item("#txtEmail").text = itemData.email || "E-posta Yok";
        $item("#txtYat").text = itemData.yat || "Yat Belirtilmemiş";
        $item("#txtMesaj").text = itemData.mesaj || "Detay Yok";
    });

    // ---------- İLETİŞİM MESAJLARI ----------
    $w("#repeaterIletisim").onItemReady(($item, itemData) => {
        $item("#txtIletisimIsim").text = itemData.isim || "İsim Yok";
        $item("#txtIletisimEmail").text = itemData.email || "E-posta Yok";
        $item("#txtIletisimMesaj").text = itemData.mesaj || "Mesaj Yok";
    });

    // ---------- GİRİŞ ----------
    $w("#girisButton").onClick(() => girisYap());
    $w("#sifreInput").onKeyPress((event) => {
        if (event.key === "Enter") girisYap();
    });
});

async function girisYap() {
    const sifre = $w("#sifreInput").value;
    if (!sifre) {
        $w("#girisHata").text = "Lütfen şifreyi girin.";
        return;
    }

    $w("#girisButton").disable();
    $w("#girisHata").text = "Kontrol ediliyor...";

    try {
        const sonuc = await getDashboardData(sifre);

        if (!sonuc.basari) {
            $w("#girisHata").text = "Şifre hatalı.";
            return;
        }

        $w("#girisHata").text = "";
        $w("#sifreInput").collapse();
        $w("#girisButton").collapse();
        verileriGoster(sonuc);
    } catch (err) {
        console.log("Giriş hatası:", err);
        $w("#girisHata").text = "Bir hata oluştu, tekrar deneyin.";
    } finally {
        $w("#girisButton").enable();
    }
}

function verileriGoster(sonuc) {
    // Rezervasyonlar (Wix CMS) + chatbot kayıtları (Render API) aynı listede
    const hepsi = [
        ...sonuc.rezervasyonlar.map(normalize),
        ...sonuc.chatbot.map(l => normalize({ ...l, _id: "api-" + l._id }))
    ];
    console.log("Toplam rezervasyon:", hepsi.length);
    if (hepsi.length > 0) {
        $w("#repeaterLeads").data = hepsi;
        $w("#repeaterLeads").expand();
    }

    const iletisimKayitlar = sonuc.iletisim.map(iletisimNormalize);
    console.log("Toplam iletişim mesajı:", iletisimKayitlar.length);
    if (iletisimKayitlar.length > 0) {
        $w("#repeaterIletisim").data = iletisimKayitlar;
        $w("#repeaterIletisim").expand();
    }
}

// ================= REZERVASYON =================

function normalize(k) {
    const tarih = k.tarih || k.date || k._createdDate;
    return {
        _id: String(k._id),
        isim: k.isim || k.adSoyad || k.name || k.ad || k.title,
        telefon: k.telefon || k.phone || k.tel,
        email: k.email || k.ePosta || k.eposta || k.mail || k.emailAdresi,
        yat: yatBul(k),
        mesaj: [k.mesaj || k.message || k.not, tarih ? new Date(tarih).toLocaleString("tr-TR") : null, k.port || k.liman]
            .filter(Boolean).join(" • ")
    };
}

function yatBul(k) {
    const anahtar = Object.keys(k).find(a => /yat|tekne|yacht|boat/i.test(a));
    if (!anahtar) return null;
    const deger = k[anahtar];
    if (deger && typeof deger === "object") return deger.title || deger.isim || deger.ad || null;
    return deger;
}

// ================= İLETİŞİM =================

function iletisimNormalize(k) {
    const mesaj = alanBul(k, /mesaj|message|not|aciklama|açıklama|konu|subject/i);
    const tarih = k._createdDate ? new Date(k._createdDate).toLocaleString("tr-TR") : null;
    return {
        _id: String(k._id),
        isim: adSoyadBul(k),
        email: alanBul(k, /mail|posta/i),
        mesaj: [mesaj, tarih].filter(Boolean).join(" • ")
    };
}

// Kalıba uyan ilk dolu alanı bulur (Wix'in sistem alanlarını atlar)
function alanBul(k, kalip) {
    const anahtar = Object.keys(k).find(a => !a.startsWith("_") && kalip.test(a) && k[a]);
    return anahtar ? String(k[anahtar]) : null;
}

// Ad ve soyadı birleştirir ("Ali" + "Yılmaz" → "Ali Yılmaz")
function adSoyadBul(k) {
    const anahtarlar = Object.keys(k).filter(a => !a.startsWith("_") && k[a]);

    const tekAlan = anahtarlar.find(a => /adsoyad|fullname|isimsoyisim/i.test(a));
    if (tekAlan) return String(k[tekAlan]);

    const ad = anahtarlar.find(a => /^(ad|isim|name|first|title)/i.test(a) && !/adres|soyad|soyisim/i.test(a));
    const soyad = anahtarlar.find(a => /soyad|soyisim|surname|last/i.test(a));

    return [ad && k[ad], soyad && k[soyad]].filter(Boolean).join(" ") || null;
}
