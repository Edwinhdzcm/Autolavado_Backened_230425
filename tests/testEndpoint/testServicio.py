import uuid
import datetime

import pytest
from fastapi.testclient import TestClient

from main import app
from config.db import SessionLocal
from models.model_services import Servicio
import auth

# Override para evitar autenticación
def override_get_current_user():
	return "test_user"

app.dependency_overrides[auth.get_current_user] = override_get_current_user


def test_crear_servicio_exitoso():
	"""Test para crear un servicio exitosamente"""
	client = TestClient(app)
	db = SessionLocal()
	servicio_id = None
	
	try:
		# Preparar datos únicos
		nombre_servicio = f"Servicio_{uuid.uuid4().hex[:8]}"
		payload = {
			"nombre_servicio": nombre_servicio,
			"descripcion": "Servicio de prueba",
			"precio": 99.99,
			"estado": True,
			"fecha_registro": datetime.datetime.utcnow().isoformat(),
			"fecha_actualizacion": datetime.datetime.utcnow().isoformat()
		}
		
		# Hacer POST al endpoint
		response = client.post("/servicio/", json=payload)
		
		# Verificar respuesta exitosa
		assert response.status_code == 200, f"Error: {response.text}"
		data = response.json()
		assert data.get("nombre_servicio") == nombre_servicio
		assert data.get("precio") == 99.99
		servicio_id = data.get("Id")
		assert isinstance(servicio_id, int)
		
		# Verificar que se guardó en la BD
		db_verify = SessionLocal()
		servicio_en_bd = db_verify.query(Servicio).filter(Servicio.nombre_servicio == nombre_servicio).first()
		db_verify.close()
		
		assert servicio_en_bd is not None, f"El servicio '{nombre_servicio}' NO se guardó en la BD"
		assert servicio_en_bd.precio == 99.99
		
	finally:
		try:
			db.close()
		except:
			pass


def test_listar_servicios():
	"""Test para listar todos los servicios"""
	client = TestClient(app)
	
	# GET debe retornar lista de servicios
	response = client.get("/servicio/")
	
	assert response.status_code == 200, f"Error: {response.text}"
	data = response.json()
	assert isinstance(data, list), "Se esperaba una lista de servicios"
	
	# Puede estar vacía o tener elementos
	for servicio in data:
		assert "Id" in servicio
		assert "nombre_servicio" in servicio
		assert "precio" in servicio
