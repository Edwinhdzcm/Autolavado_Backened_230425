import uuid
import datetime

import pytest
from fastapi.testclient import TestClient

from main import app
from config.db import SessionLocal
from models.model_rol import Rol
from models.model_usuario import Usuario


def test_login_usuario_exitoso():
	"""Test para login exitoso de usuario"""
	client = TestClient(app)
	db_setup = SessionLocal()
	usuario_id = None
	rol_id = None
	
	try:
		# 1. Crear un rol
		nombre_rol = f"testrole_{uuid.uuid4().hex[:6]}"
		rol = Rol(
			nombre_rol=nombre_rol,
			estado=True,
			fecha_registro=datetime.datetime.utcnow(),
			fecha_actualizacion=datetime.datetime.utcnow(),
		)
		db_setup.add(rol)
		db_setup.commit()
		db_setup.refresh(rol)
		rol_id = rol.Id
		
		# 2. Crear un usuario
		nombre_usuario = f"user_{uuid.uuid4().hex[:8]}"
		correo = f"{nombre_usuario}@test.com"
		contraseña = "Mi_Password_123"
		now_iso = datetime.datetime.utcnow().isoformat()
		
		payload_registro = {
			"rol_Id": rol_id,
			"nombre": nombre_usuario,
			"primer_apellido": "Test",
			"segundo_apellido": "User",
			"direccion": "Calle Test 123",
			"correo_electronico": correo,
			"numero_telefono": "5551234567",
			"contrasena": contraseña,
			"estado": True,
			"fecha_registro": now_iso,
			"fecha_actualizacion": now_iso,
		}
		
		response_registro = client.post("/usuario/", json=payload_registro)
		assert response_registro.status_code == 200, f"Error en registro: {response_registro.text}"
		usuario_id = response_registro.json().get("Id")
		
		# 3. Intentar login con correo
		login_payload = {
			"username": correo,  # El endpoint espera username pero acepta correo
			"password": contraseña,
		}
		
		# Login espera form-data, no JSON
		response_login = client.post("/login/", data=login_payload)
		assert response_login.status_code == 200, f"Error en login: {response_login.text}"
		
		data = response_login.json()
		assert "access_token" in data, "No se generó token"
		assert data.get("token_type") == "bearer"
		
	finally:
		try:
			db_setup.close()
		except:
			pass


def test_login_usuario_credenciales_incorrectas():
	"""Test para login fallido con credenciales incorrectas"""
	client = TestClient(app)
	db_setup = SessionLocal()
	usuario_id = None
	rol_id = None
	
	try:
		# 1. Crear rol y usuario
		nombre_rol = f"testrole_{uuid.uuid4().hex[:6]}"
		rol = Rol(
			nombre_rol=nombre_rol,
			estado=True,
			fecha_registro=datetime.datetime.utcnow(),
			fecha_actualizacion=datetime.datetime.utcnow(),
		)
		db_setup.add(rol)
		db_setup.commit()
		db_setup.refresh(rol)
		rol_id = rol.Id
		
		nombre_usuario = f"user_{uuid.uuid4().hex[:8]}"
		correo = f"{nombre_usuario}@test.com"
		contraseña_correcta = "Mi_Password_123"
		now_iso = datetime.datetime.utcnow().isoformat()
		
		payload_registro = {
			"rol_Id": rol_id,
			"nombre": nombre_usuario,
			"primer_apellido": "Test",
			"segundo_apellido": "User",
			"direccion": "Calle Test 123",
			"correo_electronico": correo,
			"numero_telefono": "5551234567",
			"contrasena": contraseña_correcta,
			"estado": True,
			"fecha_registro": now_iso,
			"fecha_actualizacion": now_iso,
		}
		
		response_registro = client.post("/usuario/", json=payload_registro)
		assert response_registro.status_code == 200
		usuario_id = response_registro.json().get("Id")
		
		# 2. Intentar login con contraseña incorrecta
		login_payload = {
			"username": correo,
			"password": "Contraseña_Incorrecta",
		}
		
		response_login = client.post("/login/", data=login_payload)
		assert response_login.status_code == 401, f"Se esperaba 401 pero se obtuvo {response_login.status_code}"
		assert "incorrectas" in response_login.json().get("detail", "").lower()
		
	finally:
		try:
			db_setup.close()
		except:
			pass
