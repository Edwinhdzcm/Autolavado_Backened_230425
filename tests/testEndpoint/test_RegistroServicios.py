import uuid
import pytest
from fastapi.testclient import TestClient
from main import app
import auth

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_auth():
    def override_get_current_user():
        return "test_user"
    app.dependency_overrides[auth.get_current_user] = override_get_current_user
    yield
    app.dependency_overrides = {}

def test_crear_servicio_exitoso():
    nombre_unico = f"Servicio_{uuid.uuid4().hex[:4]}"
    payload = {
        "nombre": nombre_unico,
        "descripcion": "Descripción de prueba",
        "costo": 99.99,
        "duracion_minutos": 60,
        "estado": True
    }
    # Intentamos /servicios/ o /servicio/ según tu router
    response = client.post("/servicios/", json=payload)
    if response.status_code == 404:
        response = client.post("/servicio/", json=payload)
        
    assert response.status_code == 201
    assert response.json()["nombre"] == nombre_unico

def test_obtener_servicios():
    response = client.get("/servicios/")
    if response.status_code == 404:
        response = client.get("/servicio/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)