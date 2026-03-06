import uuid
import datetime

import pytest
from fastapi.testclient import TestClient

from main import app
from config.db import SessionLocal
from models.model_rol import Rol
import auth

@pytest.fixture(autouse=True)
def override_auth():
    def override_get_current_user():
        return "test_user"
    app.dependency_overrides[auth.get_current_user] = override_get_current_user
    yield
    app.dependency_overrides = {}


def test_crear_rol_exitoso():
	"""Test para crear un rol exitosamente"""
	client = TestClient(app)
	db = SessionLocal()
	rol_id_creado = None
	
	try:
		# Preparar datos únicos
		nombre_rol_unico = f"Admin_{uuid.uuid4().hex[:4]}"
		payload = {
			"nombre_rol": nombre_rol_unico,
			"estado": True,
			"fecha_registro": datetime.datetime.now(datetime.timezone.utc).isoformat(),
			"fecha_actualizacion": datetime.datetime.now(datetime.timezone.utc).isoformat()
		}
		
		# Hacer POST al endpoint
		response = client.post("/rol/", json=payload)
		
		# Verificar respuesta exitosa
		assert response.status_code == 200, f"Error: {response.text}"
		data = response.json()
		assert data.get("nombre_rol") == nombre_rol_unico
		assert data.get("estado") == True
		assert "fecha_registro" in data
		assert "fecha_actualizacion" in data
		rol_id_creado = data.get("Id")
		assert isinstance(rol_id_creado, int)
		
		# Verificar que se guardó en la BD
		db_verify = SessionLocal()
		rol_en_bd = db_verify.query(Rol).filter(Rol.nombre_rol == nombre_rol_unico).first()
		db_verify.close()
		
		assert rol_en_bd is not None, f"El rol '{nombre_rol_unico}' NO se guardó en la BD"
		assert rol_en_bd.estado == True
		
	finally:
		# Nota: NO limpiamos para que los datos persistan
		try:
			db.close()
		except:
			pass


def test_crear_rol_duplicado_falla():
	"""Test que verifica que no se puede crear un rol duplicado"""
	client = TestClient(app)
	db = SessionLocal()
	rol_id = None
	
	try:
		# Crear primer rol
		nombre_rol_unico = f"DR_{uuid.uuid4().hex[:4]}"
		payload1 = {
			"nombre_rol": nombre_rol_unico,
			"estado": True,
			"fecha_registro": datetime.datetime.now(datetime.timezone.utc).isoformat(),
			"fecha_actualizacion": datetime.datetime.now(datetime.timezone.utc).isoformat()
		}
		
		response1 = client.post("/rol/", json=payload1)
		assert response1.status_code == 200
		rol_id = response1.json().get("Id")
		
		# Intentar crear rol con el mismo nombre
		response2 = client.post("/rol/", json=payload1)
		
		# Debe fallar
		assert response2.status_code == 400, f"Se esperaba error 400 pero se obtuvo {response2.status_code}"
		assert "existente" in response2.json().get("detail", "").lower()
		
	finally:
		try:
			db.close()
		except:
			pass

