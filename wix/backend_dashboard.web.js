// WIX BACKEND KODU
// Wix'te: Kod paneli > Backend > yeni dosya: dashboard.web.js  — bu kodu içine yapıştır.
// Render'daki Python API'sine gizli anahtarla GET isteği atar ve JSON verisini döndürür.
// Anahtar burada (sunucuda) kaldığı için ziyaretçiler göremez.

import { Permissions, webMethod } from 'wix-web-module';
import { fetch } from 'wix-fetch';
import { getSecret } from 'wix-secrets-backend';

// Render'daki servisinin adresi + /api/dashboard
const API_URL = 'https://RENDER-ADRESIN.onrender.com/api/dashboard';

// Permissions.Admin: sadece site sahibi / ortak çalışanlar (giriş yapmış) çağırabilir
export const getDashboardData = webMethod(Permissions.Admin, async () => {
    const apiKey = await getSecret('NAVTERA_API_KEY');

    const response = await fetch(API_URL, {
        method: 'get',
        headers: { 'X-API-Key': apiKey }
    });

    if (!response.ok) {
        throw new Error(`API hatası: ${response.status}`);
    }

    const json = await response.json();
    return json.data; // [{ _id, isim, telefon, mesaj, tarih }, ...]
});
