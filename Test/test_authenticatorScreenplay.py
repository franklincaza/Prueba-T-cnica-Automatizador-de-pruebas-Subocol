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
    """Carga los datos desde login_data.json de manera dinámica."""
    with open("login_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.parametrize("test_case", [data["input"]["email"] for data in json.load(open("login_data.json"))])
def test_login(actor, mock_url, load_test_data, test_case, caplog):
    """Itera sobre los datos del JSON y valida el login con más validaciones."""
    with caplog.at_level(logging.INFO):
        logger.info(f"\U0001F539 Ejecutando prueba para el email: {test_case}")
        
        input_data = next((data for data in load_test_data if data["input"]["email"] == test_case), None)
        if not input_data:
            pytest.fail(f"\u274c No se encontró el caso de prueba para el email: {test_case}")

        expected_sessionid = input_data.get("session", {}).get("sessionid", None)
        expected_status = 200 if expected_sessionid else 401
        
        with requests_mock.Mocker() as m:
            if expected_status == 200:
                m.post(mock_url, json={"session": {"sessionid": expected_sessionid}}, status_code=200)
                logger.info(f"\u2705 Simulando respuesta de éxito con sessionid {expected_sessionid}")
            else:
                m.post(mock_url, json={"error": "Unauthorized"}, status_code=401)
                logger.warning(f"\u26d4 Simulando error 401 para login fallido")

        session_id = LoginTask(
            input_data["input"]["email"],
            input_data["input"]["password"],
            input_data["input"]["tokenReCaptcha"]
        ).perform_as(actor)

        assert (session_id == expected_sessionid) == (expected_status == 200), \
            f"\u274c Fallo en el caso: {test_case}. Esperado: {expected_sessionid}, Recibido: {session_id}"
        
        logger.info(f"\U0001F539 Prueba completada para {test_case}\n")
