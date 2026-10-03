"""
app/__init__.py — Uygulama Fabrikası (Application Factory Pattern)
==================================================================
Flask'ın Application Factory deseni:
    - Birden fazla uygulama örneği oluşturmayı mümkün kılar (test için kritik!)
    - Modüller arası döngüsel import sorununu ortadan kaldırır
    - Tüm uzantıları (extensions) merkezi bir noktada başlatır

Bu dosya DİREKT iş mantığı içermez. Sadece parçaları bir araya getirir.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config_selector, Config
from app.database import init_db


def create_app(config_name: str = None) -> Flask:
    """
    Flask uygulama fabrikası.

    Args:
        config_name: 'development', 'production', 'testing'
                     None ise FLASK_ENV ortam değişkenine bakılır.

    Returns:
        Yapılandırılmış Flask uygulama örneği.
    """

    # ── 1. Flask Uygulamasını Oluştur ────────────────────────────────────────
    app = Flask(__name__)

    # ── 2. Yapılandırmayı Yükle ──────────────────────────────────────────────
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    selected_config = config_selector.get(config_name, config_selector["development"])
    app.config.from_object(selected_config)

    # ── 3. CORS'u Etkinleştir ────────────────────────────────────────────────
    # Wix frontend'in sorunsuz istek atabilmesi için tüm domainlere izin veriyoruz
    CORS(app)

    # ── 4. Veritabanını Başlat ───────────────────────────────────────────────
    # Uygulama bağlamı (app context) içinde çalışması gerekiyor
    with app.app_context():
        init_db(app)

    # ── 5. Blueprint'leri (Route gruplarını) Kaydet ──────────────────────────
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    from app.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # ── 6. Ana Sayfa ve Sağlık Kontrol Endpoint'leri ─────────────────────────
    @app.route("/")
    def root():
        """Render linki açıldığında 404 yerine servis durumunu gösterir."""
        return jsonify({"status": "SmartLead AI çalışıyor"}), 200

    @app.route("/health")
    def health_check():
        """Render / AWS / GCP'nin "uygulama ayakta mı?" sorusuna cevap verir."""
        return jsonify({"status": "ok"}), 200

    return app