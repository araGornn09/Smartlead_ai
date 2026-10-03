// WIX SAYFA KODU — "Yönetim Paneli" (giriş) sayfası > Sayfa Kodu
//
// Sayfada olması gereken elemanlar (ID'leri):
//   #kullaniciInput → Metin girişi (kullanıcı adı)
//   #sifreInput     → Metin girişi, türü "Şifre"
//   #girisButton    → Buton ("Giriş Yap")
//   #girisHata      → Metin (hata mesajları için)

import { girisYap } from 'backend/dashboard.web';
import { session } from 'wix-storage-frontend';
import wixLocationFrontend from 'wix-location-frontend';

const DASHBOARD_URL = '/dashboard'; // Dashboard sayfasının URL'si

$w.onReady(function () {
    $w("#girisHata").text = "";

    // Zaten giriş yapılmışsa direkt dashboard'a geç
    if (session.getItem("adminToken")) {
        wixLocationFrontend.to(DASHBOARD_URL);
        return;
    }

    $w("#girisButton").onClick(() => giris());
    $w("#sifreInput").onKeyPress((event) => {
        if (event.key === "Enter") giris();
    });
});

async function giris() {
    const kullaniciAdi = $w("#kullaniciInput").value;
    const sifre = $w("#sifreInput").value;

    if (!kullaniciAdi || !sifre) {
        $w("#girisHata").text = "Kullanıcı adı ve şifreyi girin.";
        return;
    }

    $w("#girisButton").disable();
    $w("#girisHata").text = "Kontrol ediliyor...";

    try {
        const sonuc = await girisYap(kullaniciAdi, sifre);
        if (!sonuc.basari) {
            $w("#girisHata").text = "Kullanıcı adı veya şifre hatalı.";
            return;
        }
        // Giriş anahtarı sadece bu sekme açıkken saklanır
        session.setItem("adminToken", sonuc.token);
        wixLocationFrontend.to(DASHBOARD_URL);
    } catch (err) {
        console.log("Giriş hatası:", err);
        $w("#girisHata").text = "Bir hata oluştu, tekrar deneyin.";
    } finally {
        $w("#girisButton").enable();
    }
}
