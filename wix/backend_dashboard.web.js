// WIX BACKEND KODU — Arka Uç + Açık Kod > Backend > dashboard.web.js
// Dashboard girişi burada (sunucuda) kontrol edilir. Şifre doğruysa
// rezervasyon + iletişim (Wix CMS) ve chatbot (Render Python API) verileri döner.
// Şifre ve API anahtarı Gizli Anahtar Yöneticisi'nde durur, ziyaretçi göremez.

import { Permissions, webMethod } from 'wix-web-module';
import { fetch } from 'wix-fetch';
import { getSecret } from 'wix-secrets-backend';
import wixData from 'wix-data';

const API_URL = 'https://smartlead-ai-qbvz.onrender.com/api/dashboard';
const REZERVASYON_KOLEKSIYON = 'Rezervasyon';
const ILETISIM_KOLEKSIYON = 'Iletisim'; // CMS'teki Koleksiyon ID'si

// Dashboard girişi: şifre yanlışsa hiçbir veri dönmez
export const getDashboardData = webMethod(Permissions.Anyone, async (sifre) => {
    const gercekSifre = await getSecret('DASHBOARD_PASSWORD');

    if (!gercekSifre || typeof sifre !== 'string' || sifre !== gercekSifre) {
        // Şifre denemeyi yavaşlatmak için kısa bekleme
        await new Promise(resolve => setTimeout(resolve, 1500));
        return { basari: false };
    }

    const [rezervasyonlar, iletisim, chatbot] = await Promise.all([
        koleksiyonGetir(REZERVASYON_KOLEKSIYON),
        koleksiyonGetir(ILETISIM_KOLEKSIYON),
        chatbotKayitlari()
    ]);

    return { basari: true, rezervasyonlar, iletisim, chatbot };
});

// Wix CMS koleksiyonunu okur (suppressAuth: koleksiyon izinlerini backend'de atlar)
async function koleksiyonGetir(koleksiyon) {
    try {
        const sonuc = await wixData.query(koleksiyon)
            .descending('_createdDate')
            .limit(100)
            .find({ suppressAuth: true });
        return sonuc.items;
    } catch (err) {
        console.log(`${koleksiyon} koleksiyon hatası:`, err);
        return [];
    }
}

// Render'daki Python API'sine gizli anahtarla GET isteği atar, JSON verisini döndürür
async function chatbotKayitlari() {
    try {
        const apiKey = await getSecret('NAVTERA_API_KEY');
        const response = await fetch(API_URL, {
            method: 'get',
            headers: { 'X-API-Key': apiKey }
        });
        if (!response.ok) {
            console.log('API hatası:', response.status);
            return [];
        }
        const json = await response.json();
        return json.data || []; // [{ _id, isim, telefon, mesaj, tarih }, ...]
    } catch (err) {
        console.log('API bağlantı hatası:', err);
        return [];
    }
}
