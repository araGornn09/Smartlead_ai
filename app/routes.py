import re
from flask import Blueprint, request, jsonify, current_app, render_template
from app.database import save_lead, get_all_leads
from app.services.ai_service import ai_service, AIServiceError
from app.auth import api_admin_required

# Blueprint tanımlamaları (Hatanın çözümü buradaki isimlerdir)
api_bp = Blueprint('api', __name__)
main_bp = Blueprint('main', __name__)

# ---------------------------------------------------------
# Sayfa Rotaları
# ---------------------------------------------------------
@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

# ---------------------------------------------------------
# API Uç Noktaları
# ---------------------------------------------------------
@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    try:
        data = request.get_json()
        if not data or 'mesaj' not in data:
            return jsonify({"basari": False, "hata": "Mesaj alanı zorunludur."}), 400
        
        mesaj = data.get('mesaj')
        gecmis = temiz_gecmis(data.get('gecmis', []))

        # Mesajda telefon varsa müşteriyi otomatik kaydet (dashboard'da görünsün)
        try:
            musteri_radari(str(mesaj))
        except Exception as e:
            current_app.logger.error(f"Lead kaydedilemedi: {e}")

        yanit = ai_service(mesaj, gecmis)
        return jsonify({"basari": True, "yanit": yanit}), 200

    except AIServiceError as e:
        return jsonify({"basari": False, "hata": str(e)}), 503
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Sohbet servisinde bir hata oluştu: {str(e)}"}), 500


# Mesajda telefon numarası geçerse otomatik müşteri kaydı oluşturan "radar"
TELEFON_REGEX = re.compile(r'0?\s*5\d{2}\s*\d{3}\s*\d{2}\s*\d{2}')
TARIH_REGEX = re.compile(r'\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}')
LIMANLAR = ["istanbul", "bodrum", "göcek", "gocek", "fethiye", "marmaris", "antalya", "izmir", "çeşme", "cesme"]


def musteri_radari(mesaj):
    """Mesajdan isim, telefon, liman ve tarihi cımbızlayıp lead olarak kaydeder."""
    telefon_match = TELEFON_REGEX.search(mesaj)
    if not telefon_match:
        return

    telefon = telefon_match.group(0).strip()

    # İsim: telefondan önceki ilk satır (uzunsa son iki kelime)
    once = mesaj[:telefon_match.start()].strip().split('\n')[0].strip()
    kelimeler = once.split()
    isim = " ".join(kelimeler[-2:]) if len(kelimeler) > 3 else (once or "İsim Belirtilmedi")

    lower = mesaj.lower()
    liman = next((l.capitalize() for l in LIMANLAR if l in lower), "Belirtilmedi")
    tarih_match = TARIH_REGEX.search(mesaj)
    tarih = tarih_match.group(0) if tarih_match else "Belirtilmedi"

    save_lead(current_app, isim.title(), telefon, f"Chatbot | Liman: {liman} | Kiralama: {tarih}")


def temiz_gecmis(gecmis):
    """Wix'ten gelen sohbet geçmişini doğrular (sadece user/assistant, son 10 mesaj)."""
    if not isinstance(gecmis, list):
        return []
    return [
        {"role": m["role"], "content": m["content"][:2000]}
        for m in gecmis[-10:]
        if isinstance(m, dict) and m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str)
    ]


@api_bp.route('/chat', methods=['POST'])
def chat():
    """Wix sohbet penceresinin (navtera_chat_widget) kullandığı uç nokta: {message, history} → {response}"""
    data = request.get_json(silent=True) or {}
    mesaj = (data.get('message') or '').strip()
    if not mesaj:
        return jsonify({"response": "Lütfen geçerli bir mesaj gönderin."}), 400

    try:
        musteri_radari(mesaj)
    except Exception as e:
        current_app.logger.error(f"Lead kaydedilemedi: {e}")

    try:
        yanit = ai_service(mesaj, temiz_gecmis(data.get('history')))
        return jsonify({"response": yanit}), 200
    except AIServiceError as e:
        current_app.logger.error(str(e))
        return jsonify({"response": "Şu an yanıt veremiyorum, lütfen biraz sonra tekrar deneyin."}), 503


@api_bp.route('/leads', methods=['POST'])
def yeni_lead():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"basari": False, "hata": "Veri gönderilmedi."}), 400

        isim = data.get('isim') or data.get('name')
        telefon = data.get('telefon') or data.get('phone')
        mesaj = data.get('mesaj') or data.get('message', '')

        if not isim or not telefon:
            return jsonify({"basari": False, "hata": "İsim ve telefon zorunludur."}), 400

        kaydedilen_lead = save_lead(current_app, isim, telefon, mesaj)
        return jsonify({"basari": True, "data": kaydedilen_lead}), 201

    except Exception as e:
        return jsonify({"basari": False, "hata": f"Kayıt eklenirken hata: {str(e)}"}), 500


@api_bp.route('/leads', methods=['GET'])
@api_admin_required
def leads_listele():
    try:
        kayitlar = get_all_leads(current_app)
        return jsonify({"basari": True, "data": kayitlar}), 200

    except Exception as e:
        return jsonify({"basari": False, "hata": f"Veriler getirilemedi: {str(e)}"}), 500

@api_bp.route('/dashboard', methods=['GET'])
@api_admin_required
def dashboard_verileri():
    """
    Wix dashboard sayfası için müşteri kayıtlarını JSON olarak döndürür.
    Wix repeater'ı her satır için '_id' alanını (string) zorunlu tutar.
    Erişim: X-API-Key header'ı (Wix backend'i) veya admin oturumu.
    """
    try:
        kayitlar = get_all_leads(current_app)
        veriler = [
            {
                "_id": str(k["id"]),
                "isim": k["name"],
                "telefon": k["phone"],
                "mesaj": k.get("message") or "",
                "tarih": str(k.get("created_at") or ""),
            }
            for k in kayitlar
        ]
        return jsonify({"basari": True, "toplam": len(veriler), "data": veriler}), 200

    except Exception as e:
        return jsonify({"basari": False, "hata": f"Veriler getirilemedi: {str(e)}"}), 500
