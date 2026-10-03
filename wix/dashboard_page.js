// WIX SAYFA KODU
// Wix'te: Dashboard sayfasını aç > alttaki kod panelinde (sayfa kodu) her şeyi sil, bunu yapıştır.
//
// Sayfada olması gereken elemanlar ve ID'leri (Özellikler panelinden ID'yi değiştir):
//   #leadsRepeater  → Repeater (tekrarlayıcı)
//     İçindeki metinler:  #isimText  #telefonText  #mesajText  #tarihText
//   #toplamText     → Repeater'ın dışında, toplam kayıt sayısını yazan metin

import { getDashboardData } from 'backend/dashboard.web';

$w.onReady(async function () {
    // Her satır (müşteri) için repeater'daki metinlere veriyi yazdır
    $w('#leadsRepeater').onItemReady(($item, itemData) => {
        $item('#isimText').text = itemData.isim;
        $item('#telefonText').text = itemData.telefon;
        $item('#mesajText').text = itemData.mesaj || '-';
        $item('#tarihText').text = itemData.tarih;
    });

    try {
        const veriler = await getDashboardData();
        $w('#leadsRepeater').data = veriler;
        $w('#toplamText').text = `Toplam kayıt: ${veriler.length}`;
    } catch (err) {
        console.error(err);
        $w('#toplamText').text = 'Veriler yüklenemedi.';
    }
});
