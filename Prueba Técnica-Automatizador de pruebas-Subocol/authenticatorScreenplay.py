import requests
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class Authenticate:
    """
    Habilidad de autenticación para el actor.
    """
    def __init__(self, url):
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
            response.raise_for_status()
            data = response.json()
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

class Actor:
    """
    Representa un actor en el patrón Screenplay.
    """
    def __init__(self, name: str):
        self.name = name
        self.abilities = {}

    def can(self, ability):
        """Asigna una habilidad al actor."""
        self.abilities[type(ability)] = ability

    def use_ability(self, ability_type):
        """Obtiene una habilidad asignada al actor."""
        return self.abilities.get(ability_type, None)

class LoginTask:
    """
    Tarea para que un actor realice la autenticación.
    """
    def __init__(self, email: str, password: str, token: str):
        self.email = email
        self.password = password
        self.token = token

    def perform_as(self, actor: Actor):
        """Ejecuta la tarea de login usando la habilidad de autenticación."""
        authenticator = actor.use_ability(Authenticate)
        if authenticator:
            return authenticator.login(self.email, self.password, self.token)
        else:
            logger.error(f"{actor.name} no tiene la habilidad para autenticarse.")
            return None
