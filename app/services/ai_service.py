import re
import requests
from config import Config
from app.knowledge import build_knowledge_text

# Yat / lokasyon bilgileri ve kurallar her zaman eklenir
# (Render'da BUSINESS_CONTEXT ortam degiskeni tanimli olsa bile)
KNOWLEDGE_RULES = (
    "\n\nYATLAR VE LOKASYONLAR HAKKINDA KURALLAR:\n"
    "- Müşteri bir yatın adını yazdığında (eksik ya da hatalı yazsa bile, örn. 'riva', 'azimut', 'sunseeker') "
    "aşağıdaki bilgi tabanından o yatı bul ve TÜM bilgilerini ver: tip, uzunluk, gündüz misafir kapasitesi, "
    "konaklama kapasitesi, motor, maksimum hız ve kısa tanıtım.\n"
    "- Müşteri bir lokasyon sorduğunda (İstanbul, Bodrum, Göcek) o bölgeyi tanıt: öne çıkan yerler, rotalar ve sezon.\n"
    "- Kişi sayısı, konaklama isteği ve hız / konfor tercihine göre uygun yatları öner.\n"
    "- SADECE bilgi tabanındaki bilgileri kullan, olmayan yat veya özellik uydurma.\n"
    "- Fiyat, müsaitlik, hangi yatın hangi limanda olduğu ve kalkış marinası bilgileri sende yok. "
    "Sorulursa ekibimizin dönüş yapacağını söyle ve iletişim bilgisi iste.\n"
    "- Filoda olmayan bir yat sorulursa filomuzda olmadığını söyle ve benzer bir alternatif öner.\n"
    "- Kısa paragraflar ve '•' ile madde işaretleri kullan. Markdown KULLANMA (**, ##, tablo yok).\n"
    "- Müşteri hangi dilde yazarsa o dilde cevap ver.\n\n"
    "BİLGİ TABANI:\n"
    + build_knowledge_text()
)

class AIServiceError(Exception):
    """AI Servisi hata sınıfı"""
    pass

def ai_service(prompt, history=None):
    """
    Groq API kullanarak kullanıcının mesajına dinamik yanıt üretir.

    :param prompt: Kullanıcının gönderdiği son mesaj (str)
    :param history: Önceki sohbet geçmişi (list)
    :return: AI tarafından üretilen yanıt metni (str)
    """
    if not getattr(Config, 'GROQ_API_KEY', None):
        raise AIServiceError("Groq API anahtarı (.env / Config) tanımlanmamış.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {Config.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Sistem talimatını, şirket bağlamını ve yat / lokasyon bilgi tabanını ekliyoruz
    messages = [
        {"role": "system", "content": getattr(Config, 'BUSINESS_CONTEXT', 'Sen yardımcı bir asistansın.') + KNOWLEDGE_RULES}
    ]

    # Varsa geçmiş konuşmaları listeye ekle
    if history and isinstance(history, list):
        for msg in history:
            messages.append(msg)

    # Kullanıcının son mesajını ekle
    messages.append({"role": "user", "content": prompt})

    # Groq OpenAI uyumlu payload yapısı
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": messages,
        "max_tokens": 1500,
        "temperature": 0.4
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        res_data = response.json()

        if response.status_code != 200:
            error_msg = res_data.get('error', {}).get('message', 'Bilinmeyen API hatası')
            raise AIServiceError(f"Groq API Hatası ({response.status_code}): {error_msg}")

        # Modelin ürettiği dinamik cevabı çekip döndürüyoruz
        reply_content = res_data['choices'][0]['message']['content'] or ""
        # Wix metin alanı düz metin gösterdiği için markdown işaretlerini temizliyoruz
        reply_content = reply_content.replace("**", "")
        reply_content = re.sub(r"^#+\s*", "", reply_content, flags=re.MULTILINE)
        return reply_content.strip()

    except requests.exceptions.RequestException as e:
        raise AIServiceError(f"Bağlantı hatası oluştu: {str(e)}")
    except (KeyError, IndexError):
        raise AIServiceError("API'den beklenen formatta yanıt alınamadı.")
    except Exception as e:
        raise AIServiceError(f"AI Servis Hatası: {str(e)}")
