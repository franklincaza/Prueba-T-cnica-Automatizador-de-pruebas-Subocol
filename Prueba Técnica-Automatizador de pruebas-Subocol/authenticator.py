import requests
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class Authenticator:
    def __init__(self, url):
        """Inicializa la clase con la URL del endpoint"""
        self.url = url
        self.session_id = None
        logger.info(f"🔹 Autenticador inicializado con URL: {self.url}")

    def login(self, email, password, token_recaptcha):
        """Realiza la autenticación y extrae el sessionid"""
        payload = {
            "email": email,
            "password": password,
            "tokenReCaptcha": token_recaptcha
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        logger.info(f"📨 Enviando solicitud de login para {email}")

        try:
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()  # Lanza una excepción si hay un error HTTP

            data = response.json()  # Convertir la respuesta a JSON
            self.session_id = data.get("session", {}).get("sessionid", None)

            if self.session_id:
                logger.info(f"✅ Login exitoso. Session ID: {self.session_id}")
                return self.session_id
            else:
                logger.warning(f"⚠️ Error: No se encontró sessionid en la respuesta. Respuesta completa: {data}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error en la solicitud: {e}")
            return None
"""

# 🔹 Ejemplo de uso (descomenta para probar)
if __name__ == "__main__":
    url = "https://castlemockdemo.subocol.com/castlemock/mock/rest/project/NpJ1A9/application/eu72DD/login"  # Reemplaza con la URL real
    auth = Authenticator(url)
    
    email = "loginexitoso@subocol.com"
    password = "133deF4*"
    token_recaptcha = "03AGdBq24D1MLP7hdEJvHb2PxyzZxTu7hx4m-A7xNU7lABR-yC83NAxZONPkp"

    session_id = auth.login(email, password, token_recaptcha)
"""