# Autenticador con Patrón Screenplay en Python

Este proyecto implementa el patrón Screenplay para la autenticación de usuarios utilizando `requests` y `pytest` para las pruebas.

## 📌 Características
- Implementación del patrón Screenplay.
- Uso de `requests` para autenticación HTTP.
- Pruebas con `pytest` y `requests_mock`.
- Uso de archivos JSON para manejar datos de prueba.
- Manejo de logs para mejor trazabilidad.

## 📂 Estructura del Proyecto
```
├── authenticatorScreenplay.py   # Implementación con el patrón Screenplay
├── authenticator.py             # Implementación tradicional del autenticador
├── Test/                        # Carpeta de pruebas
│   ├── test_authenticatorScreenplay.py   # Pruebas para el patrón Screenplay
│   ├── test_authenticator.py        # Pruebas para la autenticación tradicional
├── login_data.json              # Datos de prueba para las autenticaciones
├── README.md                    # Documentación del proyecto
```

## 🚀 Instalación y Configuración
### Requisitos Previos
- Python 3.8 o superior
- `pip` instalado

### Instalación de Dependencias
Ejecuta el siguiente comando para instalar las dependencias necesarias:
```bash
pip install -r requirements.txt
```

## 🛠 Uso
### Autenticación con el Patrón Screenplay
```python
from authenticatorScreenplay import Authenticate, Actor, LoginTask

url = "https://example.com/api/login"
actor = Actor("Tester")
actor.can(Authenticate(url))

task = LoginTask("usuario@example.com", "password123", "token_recaptcha")
session_id = task.perform_as(actor)
print(f"Session ID: {session_id}")
```

### Pruebas
Ejecuta las pruebas con:
```bash
pytest -v
```

Para generar reportes en HTML con logs detallados:
```bash
pytest Test/test_authenticator.py --html=report.html --self-contained-html --log-cli-level=INFO --capture=tee-sys
pytest Test/test_authenticatorScreenplay.py --html=report_screemplay.html --log-cli-level=INFO --capture=tee-sys
pytest Test/ --html=report_screemplay.html --log-cli-level=INFO --capture=tee-sys
```

### 📌 Cómo ejecutar las pruebas
Para ejecutar las pruebas, usa `pytest` con los siguientes comandos según el alcance que desees:

1. **Ejecutar pruebas para la autenticación tradicional:**
   ```bash
   pytest Test/test_authenticator.py --html=report.html --self-contained-html --log-cli-level=INFO --capture=tee-sys
   ```
   Esto generará un reporte en `report.html` con los resultados detallados de la prueba.

2. **Ejecutar pruebas para el patrón Screenplay:**
   ```bash
   pytest Test/test_authenticatorScreenplay.py --html=report_screemplay.html --log-cli-level=INFO --capture=tee-sys
   ```
   Se generará el reporte en `report_screemplay.html` con los logs de las pruebas.

3. **Ejecutar todas las pruebas del proyecto:**
   ```bash
   pytest Test/ --html=report_screemplay.html --log-cli-level=INFO --capture=tee-sys
   ```
   Este comando ejecutará todas las pruebas contenidas en la carpeta `Test/`.

## 📌 Prueba Técnica 1: Desarrollo de un Script de Automatización en Python
### Objetivo
Verificar si el candidato puede estructurar una prueba automatizada con datos externos, aplicar correctamente el patrón Screenplay y demostrar habilidades de resolución de problemas e investigación.

### 1. Automatizar login
#### Descripción
El candidato deberá desarrollar un script en Python que permita simular el login exitoso y fallido al servicio:
```
https://castlemockdemo.subocol.com/castlemock/mock/rest/project/NpJ1A9/application/eu72DD/login
```
El servicio requiere los datos de ingreso (`session`, `email`, `password`, `tokenReCaptcha`), que deben ser leídos desde un archivo `login_data.json`.

### 2. Requerimientos
- Implementar el patrón Screenplay.
- Leer y usar datos del archivo `login_data.json`.
- Validar la respuesta (que indique si el login fue exitoso o fallido).
- Añadir comentarios explicativos sobre cualquier ajuste o investigación realizada durante el desarrollo en el `README.md`.

### 3. Archivos
#### Archivo de datos (`login_data.json`):
##### Login exitoso
```json
{
    "session": {
        "sessionid": "ca45aa1c-118e-42f6-b9c5"
    },
    "input": {
        "email": "loginexitoso@subocol.com",
        "password": "133deF4*",
        "tokenReCaptcha": "03AGdBq24D1MLP7hdEJvHb2PxyzZxTu7hx4m-A7xNU7lABR-yC83NAxZONPkp"
    }
}
```
##### Login fallido
```json
{
    "session": {
        "sessionid": "123e4567-e89b-12d3-a456-426614174000"
    },
    "input": {
        "email": "loginemailnotienecognitoidenbasededatos@subocol.com",
        "password": "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0U1v2W3x4Y5z6a7B8c9D",
        "tokenReCaptcha": "03AGdBq27GJsZ6N5ZLMn2J7B5Mv9HV2Q3-KF6QeN_U0bgDFMfpX2cEG9E9aK-Vg7CjeLwSLh5wXf7rC4QX8YGvZaVTPxNtP3JTFQkLg7cBxRu_aGNC3KJTo5MQ9w6RHRsTdDFlT_UeA5vjT4GHV_kRfMfCgDRYX9X0QD8fNLrUpVUCgV-QEjP8WZPb4jNQ9FmEdYStW7Bw6-YHYZh"
    }
}
```
### 📌 Entregables
- Archivo Python con el código de la prueba.
- Un archivo `README.md` con explicación breve del enfoque usado y cualquier ajuste implementado (documentación de investigación y toma de decisiones).

## 📄 Licencia
Este proyecto está bajo la licencia MIT.

