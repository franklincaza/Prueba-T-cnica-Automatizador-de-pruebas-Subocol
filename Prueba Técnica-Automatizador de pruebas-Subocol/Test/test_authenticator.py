import pytest
import requests_mock
import json
import logging
from authenticator import Authenticator

# Configurar logging globalmente
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test_log.log"),  # Guarda en archivo
        logging.StreamHandler()  # También muestra en consola
    ]
)
logger = logging.getLogger(__name__)

@pytest.fixture
def mock_url():
    return "https://castlemockdemo.subocol.com/castlemock/mock/rest/project/NpJ1A9/application/eu72DD/login"

@pytest.fixture
def auth_instance(mock_url):
    return Authenticator(mock_url)

@pytest.fixture
def load_test_data():
    """Carga los datos desde login_data.json"""
    with open("login_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.parametrize("test_case, expected_sessionid, expected_status", [
    ("login exitoso", "ca45aa1c-118e-42f6-b9c5", 200),
    ("login fallido", "123e4567-e89b-12d3-a456-426614174000", 401)
])
def test_login(auth_instance, mock_url, load_test_data, test_case, expected_sessionid, expected_status, caplog):
    """Itera sobre los datos y valida el login, incluyendo casos fallidos"""
    
    with caplog.at_level(logging.INFO):  # Captura logs para el reporte HTML
        logger.info(f"🔹 Ejecutando prueba: {test_case}")

        for data in load_test_data:
            if data["session"]["sessionid"] == expected_sessionid:
                input_data = data["input"]
                break
        else:
            pytest.fail(f"❌ No se encontró el caso de prueba: {test_case}")

        with requests_mock.Mocker() as m:
            if expected_status == 200:
                m.post(mock_url, json={"session": {"sessionid": expected_sessionid}}, status_code=200)
                logger.info(f"✅ Simulando respuesta de éxito con sessionid {expected_sessionid}")
            else:
                m.post(mock_url, json={"error": "Unauthorized"}, status_code=401)
                logger.warning(f"⛔ Simulando error 401 para login fallido")

            session_id = auth_instance.login(input_data["email"], input_data["password"], input_data["tokenReCaptcha"])

            if expected_status == 200:
                assert session_id == expected_sessionid, f"❌ Fallo en {test_case}: esperado {expected_sessionid}, recibido {session_id}"
                logger.info(f"✅ {test_case} pasó correctamente con session_id: {session_id}")
            else:
                assert session_id is None, f"❌ Fallo en {test_case}: se esperaba None, pero se recibió {session_id}"
                logger.warning(f"⛔ {test_case} falló correctamente como se esperaba")

        logger.info(f"🔹 Prueba completada: {test_case}\n")

