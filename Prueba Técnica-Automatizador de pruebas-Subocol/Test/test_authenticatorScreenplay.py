
from authenticatorScreenplay import Authenticate, Actor, LoginTask
import requests
import logging
import pytest
import requests_mock
import json
from typing import Any

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class Actor:
    """
    Representa un actor en el patrón Screenplay.
    """
    def __init__(self, name: str):
        self.name = name
        self.abilities = {}

    def can(self, ability: Any):
        """Asigna una habilidad al actor."""
        self.abilities[type(ability)] = ability

    def use_ability(self, ability_type: Any):
        """Obtiene una habilidad asignada al actor."""
        return self.abilities.get(ability_type, None)

class LoginTask:
    """
    Clase que representa la acción de autenticación.
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

# Tests usando pytest y requests_mock
@pytest.fixture
def mock_url():
    return "https://castlemockdemo.subocol.com/castlemock/mock/rest/project/NpJ1A9/application/eu72DD/login"

@pytest.fixture
def actor(mock_url):
    actor = Actor("Tester")
    actor.can(Authenticate(mock_url))
    return actor

@pytest.fixture
def load_test_data():
    """Carga los datos desde login_data.json"""
    with open("login_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.parametrize("test_case, expected_sessionid, expected_status", [
    ("login exitoso", "ca45aa1c-118e-42f6-b9c5", 200),
    ("login fallido", None, 401)
])
def test_login(actor, mock_url, load_test_data, test_case, expected_sessionid, expected_status, caplog):
    """Itera sobre los datos y valida el login, incluyendo casos fallidos"""
    with caplog.at_level(logging.INFO):
        logger.info(f"\U0001F539 Ejecutando prueba: {test_case}")

        input_data = None
        for data in load_test_data:
            if data["input"]["email"] == ("loginexitoso@subocol.com" if test_case == "login exitoso" else "loginemailnotienecognitoidenbasededatos@subocol.com"):
                input_data = data["input"]
                break
        
        if not input_data:
            pytest.fail(f"\u274c No se encontró el caso de prueba: {test_case}")

        with requests_mock.Mocker() as m:
            if expected_status == 200:
                m.post(mock_url, json={"session": {"sessionid": expected_sessionid}}, status_code=200)
                logger.info(f"\u2705 Simulando respuesta de éxito con sessionid {expected_sessionid}")
            else:
                m.post(mock_url, json={"error": "Unauthorized"}, status_code=401)
                logger.warning(f"\u26d4 Simulando error 401 para login fallido")

        session_id = LoginTask(
            input_data["email"],
            input_data["password"],
            input_data["tokenReCaptcha"]
        ).perform_as(actor)

        if expected_status == 200:
            assert session_id == expected_sessionid, f"\u274c Fallo en {test_case}: esperado {expected_sessionid}, recibido {session_id}"
            logger.info(f"\u2705 {test_case} pasó correctamente con session_id: {session_id}")
        else:
            assert session_id is None, f"\u274c Fallo en {test_case}: se esperaba None, pero se recibió {session_id}"
            logger.warning(f"\u26d4 {test_case} falló correctamente como se esperaba")

        logger.info(f"\U0001F539 Prueba completada: {test_case}\n")