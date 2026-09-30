"""
config.py — Merkezi Yapılandırma Yönetimi
==========================================
Tüm ortam değişkenleri ve sabit ayarlar BURADAN okunur.
Hiçbir kod dosyası doğrudan os.environ okumaz; hepsi bu sınıfı kullanır.
"""

import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()


class Config:
    """Temel yapılandırma sınıfı — tüm ortamlar bu sınıftan türer."""

    # ── Güvenlik ────────────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

    # ── Veritabanı ──────────────────────────────────────────────────────────
    SQLITE_DB_PATH = os.environ.get("SQLITE_DB_PATH", "smartlead.db")

    # ── Yapay Zekâ API ──────────────────────────────────────────────────────
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

    # Hangi AI sağlayıcı kullanılacak
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")

    # ── İşletme Kimliği (System Prompt'un temeli) ───────────────────────────
    BUSINESS_NAME = os.environ.get("BUSINESS_NAME", "NAVTERA")
    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        (
            """Sen Navtera'nın yapay zeka asistanısın. Navtera, Türkiye genelinde 
birden fazla limanda hizmet veren, kaptanlı/VIP segmentte konumlanan bir lüks yat 
kiralama markasıdır.

Görevlerin:
- Ziyaretçilere filodaki yatlar hakkında bilgi vermek (kapasite, özellikler, hangi 
  limanda bulundukları, kaptanlı/kaptansız seçenekler).
- Müşteri şikayet ve önerilerini nazikçe dinlemek ve not almak.
- Sohbet sırasında şikayet/öneri bırakan kişinin ismini ve iletişim bilgisini 
  (telefon veya e-posta) nazikçe sorup toplamak, böylece ekip geri dönüş yapabilsin.

ASLA yapma:
- Rezervasyon işlemi yapma veya rezervasyon onayı verme. Rezervasyon isteyen 
  ziyaretçiyi kibarca sitedeki Rezervasyon sayfasına yönlendir.

Ton: Sakin, özgüvenli, misafir odaklı, net ve abartısız. Türkçe konuş."""
        ),
    )

    # ── CORS İzin Verilen Kaynaklar ──────────────────────────────────────────
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")


class DevelopmentConfig(Config):
    """Geliştirme ortamı — debug açık, verbose loglar."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production ortamı — debug kapalı, güvenlik maksimum."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Test ortamı — in-memory veritabanı kullanılır."""
    DEBUG = True
    TESTING = True
    SQLITE_DB_PATH = ":memory:"


# Ortam adına göre yapılandırma seçici
config_selector = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}