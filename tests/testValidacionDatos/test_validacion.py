import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime
import uuid
import pytest
import auth

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_auth():
    def override_get_current_user():
        return "test_user"
    app.dependency_overrides[auth.get_current_user] = override_get_current_user
    yield
    app.dependency_overrides = {}

def test_crear_auto_faltan_campos():
    """Valida que falte la 'placa', la cual es obligatoria según el base model"""
    payload_incompleto = {
        "usuario_Id": 1, 
        # Falta 'placa'
        "marca": "Toyota", 
        "modelo": "Corolla", 
        "serie": "1", 
        "color": "B", 
        "tipo": "S",
        "anio": 2020, 
        "estado": True
    }
    response = client.post("/autos/", json=payload_incompleto)
    # 422 Unprocessable Entity es la respuesta por defecto de Pydantic/FastAPI ante validaciones fallidas
    assert response.status_code == 422
    assert "placa" in response.text.lower()

def test_crear_servicio_tipos_invalidos():
    """Valida enviar una cadena en vez de un flotante o entero"""
    nombre_unico = f"S_FAIL_{uuid.uuid4().hex[:4]}"
    payload_invalido = {
        "nombre": nombre_unico,
        "descripcion": "Un servicio",
        "costo": "cien dolares", # Error de tipo (espera numérico)
        "duracion_minutos": 60
    }
    response = client.post("/servicio/", json=payload_invalido)
    assert response.status_code == 422
    assert "costo" in response.text.lower()
