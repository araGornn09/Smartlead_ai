"""
app/admin.py — Admin Paneli Rotaları
=====================================
/admin/login   → Giriş sayfası
/admin         → Dashboard (müşteri kayıtları) — sadece giriş yapmış admin
/admin/logout  → Çıkış
"""

import time
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from app.auth import check_credentials, login_required, is_admin
from app.database import get_all_leads

admin_bp = Blueprint("admin", __name__)

# Basit kaba kuvvet (brute force) koruması: 5 hatalı denemede 5 dakika kilit
MAX_ATTEMPTS = 5
LOCK_SECONDS = 300
_failed_attempts = {}  # ip -> (deneme_sayisi, ilk_deneme_zamani)


def _client_ip() -> str:
    # Render bir proxy arkasında çalıştığı için gerçek IP X-Forwarded-For'da gelir
    forwarded = request.headers.get("X-Forwarded-For", "")
    return forwarded.split(",")[0].strip() if forwarded else (request.remote_addr or "")


def _is_locked(ip: str) -> bool:
    count, first = _failed_attempts.get(ip, (0, 0))
    if count >= MAX_ATTEMPTS and time.time() - first < LOCK_SECONDS:
        return True
    if time.time() - first >= LOCK_SECONDS:
        _failed_attempts.pop(ip, None)
    return False


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if is_admin():
        return redirect(url_for("admin.dashboard"))

    error = None
    if not current_app.config.get("ADMIN_PASSWORD"):
        error = "Admin girişi henüz yapılandırılmamış (ADMIN_PASSWORD tanımlı değil)."
    elif request.method == "POST":
        ip = _client_ip()
        if _is_locked(ip):
            error = "Çok fazla hatalı deneme. Lütfen 5 dakika sonra tekrar deneyin."
        elif check_credentials(request.form.get("username", ""), request.form.get("password", "")):
            _failed_attempts.pop(ip, None)
            session.clear()  # Eski oturumu temizle (session fixation koruması)
            session["is_admin"] = True
            session.permanent = True
            return redirect(url_for("admin.dashboard"))
        else:
            count, first = _failed_attempts.get(ip, (0, time.time()))
            _failed_attempts[ip] = (count + 1, first)
            error = "Kullanıcı adı veya şifre hatalı."

    return render_template("login.html", error=error)


@admin_bp.route("/", methods=["GET"])
@login_required
def dashboard():
    leads = get_all_leads(current_app)
    return render_template("dashboard.html", leads=leads)


@admin_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("admin.login"))
