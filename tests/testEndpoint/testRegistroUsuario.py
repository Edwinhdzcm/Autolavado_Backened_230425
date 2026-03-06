import uuid
import datetime

import pytest
from fastapi.testclient import TestClient

from main import app
from config.db import SessionLocal
from models.model_rol import Rol
from models.model_usuario import Usuario


def test_registro_usuario_crea_usuario_exitosa():
	"""Test de registro de usuario que verifica la creación exitosa en la BD"""
	
	# 1. Crear rol con una sesión separada
	db_setup = SessionLocal()
	role = None
	payload = None
	usuario_id_creado = None
	
	try:
		# Crear rol temporal
		nombre_rol_temp = f"testrole_{uuid.uuid4().hex[:6]}"
		role = Rol(
			nombre_rol=nombre_rol_temp,
			estado=True,
			fecha_registro=datetime.datetime.utcnow(),
			fecha_actualizacion=datetime.datetime.utcnow(),
		)
		db_setup.add(role)
		db_setup.commit()
		db_setup.refresh(role)
		role_id = role.Id
		
		# 2. Preparar datos del usuario único
		nombre_unico = f"user_{uuid.uuid4().hex[:8]}"
		correo_unico = f"{nombre_unico}@example.com"
		now_iso = datetime.datetime.utcnow().isoformat()
		
		payload = {
			"rol_Id": role_id,
			"nombre": nombre_unico,
			"primer_apellido": "Perez",
			"segundo_apellido": "Gomez",
			"direccion": "Calle Falsa 123",
			"correo_electronico": correo_unico,
			"numero_telefono": "555123456",
			"contrasena": "secreto123",
			"estado": True,
			"fecha_registro": now_iso,
			"fecha_actualizacion": now_iso,
		}
		
		# 3. Hacer POST al endpoint
		client = TestClient(app)
		response = client.post("/usuario/", json=payload)
		
		# Verificar que la respuesta fue exitosa
		assert response.status_code == 200, f"Error: {response.text}"
		data = response.json()
		assert data.get("nombre") == nombre_unico, f"Nombre no coincide: {data}"
		assert data.get("correo_electronico") == correo_unico, f"Correo no coincide: {data}"
		usuario_id_creado = data.get("Id")
		assert isinstance(usuario_id_creado, int), "El usuario debe tener un ID"
		
		# 4. Verificar que el usuario se creó REALMENTE en la BD
		# Usamos una sesión nueva para evitar caché
		db_verify = SessionLocal()
		usuario_en_bd = db_verify.query(Usuario).filter(Usuario.nombre == nombre_unico).first()
		db_verify.close()
		
		assert usuario_en_bd is not None, f"El usuario '{nombre_unico}' NO se guardó en la BD"
		assert usuario_en_bd.correo_electronico == correo_unico
		assert usuario_en_bd.Id == usuario_id_creado
		
	finally:
		# Nota: NO limpiamos para que los datos se guarden permanentemente en la BD
		try:
			db_setup.close()
		except:
			pass

