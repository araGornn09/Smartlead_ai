"""
app/auth.py — Admin Girişi ve Yetki Kontrolü
=============================================
Dashboard'a sadece giriş yapmış admin erişebilir. Kontrol tamamen
backend'de (sunucuda) yapılır; tarayıcı tarafında gizlemek yeterli değildir.
"""

import hmac
from functools import wraps
from flask import session, redirect, url_for, request, jsonify, current_app


def check_credentials(username: str, password: str) -> bool:
    """Kullanıcı adı ve şifreyi Config'teki admin bilgileriyle karşılaştırır."""
    admin_user = current_app.config.get("ADMIN_USERNAME", "")
    admin_pass = current_app.config.get("ADMIN_PASSWORD", "")
    if not admin_pass:
        return False  # Şifre tanımlanmamışsa giriş kapalı

    # compare_digest: zamanlama saldırılarına karşı güvenli karşılaştırma
    user_ok = hmac.compare_digest(username.encode(), admin_user.encode())
    pass_ok = hmac.compare_digest(password.encode(), admin_pass.encode())
    return user_ok and pass_ok


def is_admin() -> bool:
    return session.get("is_admin") is True


def has_valid_api_key() -> bool:
    """Wix backend gibi sunucudan sunucuya istekler için X-API-Key kontrolü."""
    api_key = current_app.config.get("ADMIN_API_KEY", "")
    sent_key = request.headers.get("X-API-Key", "")
    return bool(api_key) and hmac.compare_digest(sent_key.encode(), api_key.encode())


def login_required(view):
    """Sayfa rotaları için: giriş yoksa giriş sayfasına yönlendirir."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not is_admin():
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)
    return wrapped


def api_admin_required(view):
    """API rotaları için: giriş veya geçerli API anahtarı yoksa 401 döner."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not (is_admin() or has_valid_api_key()):
            return jsonify({"basari": False, "hata": "Yetkisiz erişim."}), 401
        return view(*args, **kwargs)
    return wrapped
