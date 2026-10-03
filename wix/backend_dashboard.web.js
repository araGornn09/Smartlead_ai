// WIX BACKEND KODU — Arka Uç + Açık Kod > Backend > dashboard.web.js
//
// Yönetim Paneli girişi burada (sunucuda) kontrol edilir:
//   1. girisYap(kullaniciAdi, sifre) → bilgiler doğruysa 8 saatlik bir giriş anahtarı (token) verir
//   2. getDashboardData(token)        → token geçerliyse rezervasyon + iletişim (Wix CMS)
//                                       ve chatbot (Render Python API) verilerini döndürür
// Kullanıcı adı, şifre ve API anahtarı Gizli Anahtar Yöneticisi'nde durur.

import { Permissions, webMethod } from 'wix-web-module';
import { fetch } from 'wix-fetch';
import { getSecret } from 'wix-secrets-backend';
import wixData from 'wix-data';
import { createHmac, timingSafeEqual } from 'crypto';

const API_URL = 'https://smartlead-ai-qbvz.onrender.com/api/dashboard';
const REZERVASYON_KOLEKSIYON = 'Rezervasyon';
const ILETISIM_KOLEKSIYON = 'Iletisim'; // CMS'teki Koleksiyon ID'si
const OTURUM_SURESI_MS = 8 * 60 * 60 * 1000; // 8 saat

// ================= GİRİŞ =================

export const girisYap = webMethod(Permissions.Anyone, async (kullaniciAdi, sifre) => {
    const [gercekKullanici, gercekSifre] = await Promise.all([
        getSecret('DASHBOARD_USERNAME'),
        getSecret('DASHBOARD_PASSWORD')
    ]);

    const dogru = gercekKullanici && gercekSifre
        && esitMi(String(kullaniciAdi || ''), gercekKullanici)
        && esitMi(String(sifre || ''), gercekSifre);

    if (!dogru) {
        // Şifre denemeyi yavaşlatmak için kısa bekleme
        await new Promise(resolve => setTimeout(resolve, 1500));
        return { basari: false };
    }

    const bitis = Date.now() + OTURUM_SURESI_MS;
    return { basari: true, token: `${bitis}.${imza(bitis, gercekSifre)}` };
});

// ================= DASHBOARD VERİLERİ =================

export const getDashboardData = webMethod(Permissions.Anyone, async (token) => {
    if (!(await tokenGecerliMi(token))) {
        return { basari: false };
    }

    const [rezervasyonlar, iletisim, chatbot] = await Promise.all([
        koleksiyonGetir(REZERVASYON_KOLEKSIYON),
        koleksiyonGetir(ILETISIM_KOLEKSIYON),
        chatbotKayitlari()
    ]);

    return { basari: true, rezervasyonlar, iletisim, chatbot };
});

// ================= YARDIMCI FONKSİYONLAR =================

function imza(bitis, gizli) {
    return createHmac('sha256', gizli).update(String(bitis)).digest('hex');
}

// Zamanlama saldırılarına karşı güvenli karşılaştırma
function esitMi(a, b) {
    const ba = Buffer.from(a);
    const bb = Buffer.from(b);
    return ba.length === bb.length && timingSafeEqual(ba, bb);
}

async function tokenGecerliMi(token) {
    if (typeof token !== 'string' || !token.includes('.')) return false;
    const [bitisStr, gelenImza] = token.split('.');
    const bitis = Number(bitisStr);
    if (!bitis || Date.now() > bitis) return false; // süresi dolmuş

    const gercekSifre = await getSecret('DASHBOARD_PASSWORD');
    return Boolean(gercekSifre) && esitMi(gelenImza || '', imza(bitis, gercekSifre));
}

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
