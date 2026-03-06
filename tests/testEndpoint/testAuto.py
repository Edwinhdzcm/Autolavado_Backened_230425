import uuid
import datetime

import pytest
from fastapi.testclient import TestClient

from main import app
from config.db import SessionLocal
from models.model_auto import Vehiculo
import auth

# Override para evitar autenticación
def override_get_current_user():
	return "test_user"

app.dependency_overrides[auth.get_current_user] = override_get_current_user


def test_crear_vehiculo_exitoso():
	"""Test para crear un vehículo/auto exitosamente"""
	client = TestClient(app)
	db = SessionLocal()
	vehiculo_id = None
	
	try:
		# Preparar datos únicos
		placa_unica = f"PLK{uuid.uuid4().hex[:6].upper()}"
		payload = {
			"placa": placa_unica,
			"marca": "Toyota",
			"modelo": "Corolla",
			"año": 2023,
			"color": "Blanco",
			"numero_chasis": f"CHASIS_{uuid.uuid4().hex[:10]}",
			"numero_motor": f"MOTOR_{uuid.uuid4().hex[:10]}",
			"estado": True,
			"fecha_registro": datetime.datetime.utcnow().isoformat(),
			"fecha_actualizacion": datetime.datetime.utcnow().isoformat()
		}
		
		# Hacer POST al endpoint
		response = client.post("/autos/", json=payload)
		
		# Verificar respuesta exitosa
		assert response.status_code == 200, f"Error: {response.text}"
		data = response.json()
		assert data.get("placa") == placa_unica
		assert data.get("marca") == "Toyota"
		vehiculo_id = data.get("Id")
		assert isinstance(vehiculo_id, int)
		
		# Verificar que se guardó en la BD
		db_verify = SessionLocal()
		vehiculo_en_bd = db_verify.query(Vehiculo).filter(Vehiculo.placa == placa_unica).first()
		db_verify.close()
		
		assert vehiculo_en_bd is not None, f"El vehículo con placa '{placa_unica}' NO se guardó en la BD"
		assert vehiculo_en_bd.marca == "Toyota"
		
	finally:
		try:
			db.close()
		except:
			pass


def test_crear_vehiculo_placa_duplicada():
	"""Test que verifica que no se pueda crear vehículo con placa duplicada"""
	client = TestClient(app)
	db = SessionLocal()
	
	try:
		# Crear primer vehículo
		placa_unica = f"PLK{uuid.uuid4().hex[:6].upper()}"
		payload = {
			"placa": placa_unica,
			"marca": "Toyota",
			"modelo": "Camry",
			"año": 2023,
			"color": "Negro",
			"numero_chasis": f"CHASIS_{uuid.uuid4().hex[:10]}",
			"numero_motor": f"MOTOR_{uuid.uuid4().hex[:10]}",
			"estado": True,
			"fecha_registro": datetime.datetime.utcnow().isoformat(),
			"fecha_actualizacion": datetime.datetime.utcnow().isoformat()
		}
		
		response1 = client.post("/autos/", json=payload)
		assert response1.status_code == 200
		
		# Intentar crear otro vehículo con la misma placa
		payload["numero_chasis"] = f"CHASIS_{uuid.uuid4().hex[:10]}"  # Cambiar chasis
		payload["numero_motor"] = f"MOTOR_{uuid.uuid4().hex[:10]}"   # Cambiar motor
		
		response2 = client.post("/autos/", json=payload)
		
		# Debe fallar o ser manejado según tu lógica
		# Puede ser 400 (Bad Request) o 422 (Unprocessable)
		assert response2.status_code in [400, 422], f"Se esperaba error pero se obtuvo {response2.status_code}"
		
	finally:
		try:
			db.close()
		except:
			pass


def test_listar_vehiculos():
	"""Test para listar todos los vehículos"""
	client = TestClient(app)
	
	# GET debe retornar lista de vehículos
	response = client.get("/autos/")
	
	assert response.status_code == 200, f"Error: {response.text}"
	data = response.json()
	assert isinstance(data, list), "Se esperaba una lista de vehículos"
	
	# Puede estar vacía o tener elementos
	for vehiculo in data:
		assert "Id" in vehiculo
		assert "placa" in vehiculo
		assert "marca" in vehiculo
