import pytest
import uuid
import datetime
from fastapi.testclient import TestClient
from main import app
from config.db import SessionLocal
from models.model_rol import Rol

client = TestClient(app)

@pytest.fixture(autouse=True)
def wipe_dependency_overrides():
    """Limpia los overrides en este modulo para que funcione el flujo con tokens reales"""
    app.dependency_overrides = {}
    yield

@pytest.fixture(scope="module")
def setup_test_user():
    """Fixture que crea un rol y usuario de prueba por módulo para usar su login y limpiarlos al final"""
    db = SessionLocal()
    
    # 1. Crear Rol
    rol = Rol(
        nombre_rol=f"AuthRol_{uuid.uuid4().hex[:4]}",
        estado=True,
        fecha_registro=datetime.datetime.now(datetime.timezone.utc),
        fecha_actualizacion=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(rol)
    db.commit()
    db.refresh(rol)
    
    # 2. Registrar Usuario a través de la API
    nombre = f"usr_{uuid.uuid4().hex[:4]}"
    correo = f"{nombre}@test.com"
    password = "MySecurePassword123"
    
    user_payload = {
        "rol_Id": rol.Id,
        "nombre": nombre,
        "primer_apellido": "Auth",
        "segundo_apellido": "Test",
        "direccion": "123 Calle",
        "correo_electronico": correo,
        "numero_telefono": f"555{uuid.uuid4().hex[:4]}",
        "contrasena": password,
        "estado": True,
        "fecha_registro": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "fecha_actualizacion": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    register_response = client.post("/usuario/", json=user_payload)
    assert register_response.status_code == 200
    
    yield {"correo": correo, "password": password, "rol_id": rol.Id}
    
    # Nota: No limpiamos acá por si quieres ver los datos en la BD como en los otros tests
    db.close()


def test_login_exitoso(setup_test_user):
    """Prueba que un usuario insertado puede loguearse y recibir un JWT"""
    login_data = {
        "username": setup_test_user["correo"],
        "password": setup_test_user["password"]
    }
    # fastapi OAuth2PasswordRequestForm espera form-data, no JSON
    response = client.post("/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_credenciales_invalidas(setup_test_user):
    """Prueba de login con contraseña errónea"""
    login_data = {
        "username": setup_test_user["correo"],
        "password": "WrongPassword456"
    }
    response = client.post("/login", data=login_data)
    assert response.status_code == 401
    assert "Credenciales incorrectas" in response.text

def test_acceso_recurso_protegido_con_token(setup_test_user):
    """Acceso a una ruta protegida con token JWT válido"""
    # 1. Hacer Login para sacar el token
    login_data = {
        "username": setup_test_user["correo"],
        "password": setup_test_user["password"]
    }
    login_res = client.post("/login", data=login_data)
    token = login_res.json()["access_token"]
    
    # 2. Consultar endpoint protegido con cabecera de autenticación
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/servicio/", headers=headers)
    
    # 200 OK significa que la autenticación Depends(get_current_user) pasó
    assert response.status_code == 200

def test_acceso_denegado_sin_token():
    """Acceso denegado a ruta protegida si no hay headers de autorización"""
    response = client.get("/servicio/")
    # FastAPI OAuth2PasswordBearer arroja 401 si no detecta la cabecera
    assert response.status_code == 401
