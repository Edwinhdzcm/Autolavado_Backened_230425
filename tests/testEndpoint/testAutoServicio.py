import os
import uuid
import datetime
from datetime import date, time

import pytest
from fastapi.testclient import TestClient

from main import app
from config.db import SessionLocal
from models.model_rol import Rol
from models.model_usuario import Usuario
from models.model_auto import Vehiculo
from models.model_services import Servicio
from models.model_auto_servicio import VehiculoServicio
import auth

# Override para evitar autenticación
def override_get_current_user():
	return "test_user"

app.dependency_overrides[auth.get_current_user] = override_get_current_user


def test_crear_auto_servicio_exitoso():
	"""Test para crear un servicio de auto exitosamente"""
	client = TestClient(app)
	db = SessionLocal()
	rol_id = None
	usuario_cajero_id = None
	usuario_operativo_id = None
	vehiculo_id = None
	servicio_id = None
	auto_servicio_id = None
	
	try:
		# 1. Crear rol
		nombre_rol = f"R_{uuid.uuid4().hex[:4]}"
		rol = Rol(
			nombre_rol=nombre_rol,
			estado=True,
			fecha_registro=datetime.datetime.utcnow(),
			fecha_actualizacion=datetime.datetime.utcnow(),
		)
		db.add(rol)
		db.commit()
		db.refresh(rol)
		rol_id = rol.Id
		
		# 2. Crear usuario cajero
		nombre_usuario_cajero = f"cajero_{uuid.uuid4().hex[:6]}"
		usuario_cajero = Usuario(
			rol_Id=rol_id,
			nombre=nombre_usuario_cajero,
			primer_apellido="Perez",
			segundo_apellido="Gomez",
			direccion="Calle 123",
			correo_electronico=f"cajero_{uuid.uuid4().hex[:4]}@test.com",
			numero_telefono="5551234567",
			contrasena="hashedpass",
			estado=True,
			fecha_registro=datetime.datetime.utcnow(),
			fecha_actualizacion=datetime.datetime.utcnow()
		)
		db.add(usuario_cajero)
		db.commit()
		db.refresh(usuario_cajero)
		usuario_cajero_id = usuario_cajero.Id
		
		# 3. Crear usuario operativo
		nombre_usuario_operativo = f"operativo_{uuid.uuid4().hex[:6]}"
		usuario_operativo = Usuario(
			rol_Id=rol_id,
			nombre=nombre_usuario_operativo,
			primer_apellido="Lopez",
			segundo_apellido="Garcia",
			direccion="Calle 456",
			correo_electronico=f"operativo_{uuid.uuid4().hex[:4]}@test.com",
			numero_telefono="5559876543",
			contrasena="hashedpass",
			estado=True,
			fecha_registro=datetime.datetime.utcnow(),
			fecha_actualizacion=datetime.datetime.utcnow()
		)
		db.add(usuario_operativo)
		db.commit()
		db.refresh(usuario_operativo)
		usuario_operativo_id = usuario_operativo.Id
		
		# 4. Crear vehículo
		placa_unica = f"AS{uuid.uuid4().hex[:3].upper()}"
		vehiculo = Vehiculo(
			usuario_Id=usuario_cajero_id,
			placa=placa_unica,
			modelo="Toyota Corolla",
			serie="123ABC",
			color="Blanco",
			tipo="Sedán",
			anio="2020",
			estado=True,
			fecha_registro=datetime.datetime.utcnow(),
			fecha_actualizacion=datetime.datetime.utcnow()
		)
		db.add(vehiculo)
		db.commit()
		db.refresh(vehiculo)
		vehiculo_id = vehiculo.Id
		
		# 5. Crear servicio
		nombre_servicio = f"Srv_{uuid.uuid4().hex[:4]}"
		servicio = Servicio(
			nombre_servicio=nombre_servicio,
			precio=25.50,
			descripcion="Lavado completo",
			tiempo_estimado=30,
			estado=True,
			fecha_registro=datetime.datetime.utcnow(),
			fecha_actualizacion=datetime.datetime.utcnow()
		)
		db.add(servicio)
		db.commit()
		db.refresh(servicio)
		servicio_id = servicio.Id
		
		# 6. Crear auto_servicio via endpoint
		now_iso = datetime.datetime.utcnow().isoformat()
		payload = {
			"vehiculo_Id": vehiculo_id,
			"cajero_Id": usuario_cajero_id,
			"operativo_Id": usuario_operativo_id,
			"servicio_Id": servicio_id,
			"fecha": now_iso,
			"hora": "10:30:00",
			"estatus": "Completado",
			"estado": True,
			"fecha_registro": now_iso,
			"fecha_actualizacion": now_iso
		}
		
		response = client.post("/auto-servicio/", json=payload)
		
		assert response.status_code == 201, f"Error: {response.text}"
		data = response.json()
		assert data.get("vehiculo_Id") == vehiculo_id
		assert data.get("servicio_Id") == servicio_id
		auto_servicio_id = data.get("Id")
		assert isinstance(auto_servicio_id, int)
		
		# Verificar en BD
		db_verify = SessionLocal()
		auto_servicio_en_bd = db_verify.query(VehiculoServicio).filter(VehiculoServicio.Id == auto_servicio_id).first()
		db_verify.close()
		
		assert auto_servicio_en_bd is not None, "El auto_servicio NO se guardó en la BD"
		assert auto_servicio_en_bd.vehiculo_Id == vehiculo_id
		
	finally:
		# Limpieza
		try:
			if not os.getenv("TEST_KEEP_DB"):
				db_cleanup = SessionLocal()
				if auto_servicio_id:
					db_cleanup.query(VehiculoServicio).filter(VehiculoServicio.Id == auto_servicio_id).delete(synchronize_session=False)
				if servicio_id:
					db_cleanup.query(Servicio).filter(Servicio.Id == servicio_id).delete(synchronize_session=False)
				if vehiculo_id:
					db_cleanup.query(Vehiculo).filter(Vehiculo.Id == vehiculo_id).delete(synchronize_session=False)
				if usuario_cajero_id:
					db_cleanup.query(Usuario).filter(Usuario.Id == usuario_cajero_id).delete(synchronize_session=False)
				if usuario_operativo_id:
					db_cleanup.query(Usuario).filter(Usuario.Id == usuario_operativo_id).delete(synchronize_session=False)
				if rol_id:
					db_cleanup.query(Rol).filter(Rol.Id == rol_id).delete(synchronize_session=False)
				db_cleanup.commit()
				db_cleanup.close()
		except Exception as e:
			print(f"Error en limpieza: {e}")
		
		try:
			db.close()
		except:
			pass

		
		payload_usuario = {
			"rol_Id": rol_id,
			"nombre": "TestUser",
			"primer_apellido": "Test",
			"segundo_apellido": "User",
			"direccion": "Calle Test 123",
			"correo_electronico": "correo@test.com",
			"numero_telefono": "5551234567",
			"contrasena": "Pass123!",
			"estado": True,
			"fecha_registro": now_iso,
			"fecha_actualizacion": now_iso,
		}
		
		response_usuario = client.post("/usuario/", json=payload_usuario)
		assert response_usuario.status_code == 200
		usuario_id = response_usuario.json().get("Id")
		
		# 3. Crear vehículo
		placa_unica = f"PLK{uuid.uuid4().hex[:6].upper()}"
		payload_vehiculo = {
			"placa": placa_unica,
			"marca": "Honda",
			"modelo": "Civic",
			"año": 2022,
			"color": "Rojo",
			"numero_chasis": f"CHASIS_{uuid.uuid4().hex[:10]}",
			"numero_motor": f"MOTOR_{uuid.uuid4().hex[:10]}",
			"estado": True,
			"fecha_registro": now_iso,
			"fecha_actualizacion": now_iso
		}
		
		response_vehiculo = client.post("/autos/", json=payload_vehiculo)
		assert response_vehiculo.status_code == 200
		vehiculo_id = response_vehiculo.json().get("Id")
		
		# 4. Crear servicio
		nombre_servicio = f"Servicio_{uuid.uuid4().hex[:8]}"
		payload_servicio = {
			"nombre_servicio": nombre_servicio,
			"descripcion": "Lavado y encerado",
			"precio": 150.00,
			"estado": True,
			"fecha_registro": now_iso,
			"fecha_actualizacion": now_iso
		}
		
		response_servicio = client.post("/servicio/", json=payload_servicio)
		assert response_servicio.status_code == 200
		servicio_id = response_servicio.json().get("Id")
		
		# 5. Crear relación usuario-vehículo-servicio
		payload_auto_servicio = {
			"usuario_Id": usuario_id,
			"vehiculo_Id": vehiculo_id,
			"servicio_Id": servicio_id,
			"estado": True,
			"fecha_registro": now_iso,
			"fecha_actualizacion": now_iso
		}
		
		response_auto_servicio = client.post("/usuario_vehiculo_servicio/", json=payload_auto_servicio)
		assert response_auto_servicio.status_code == 200, f"Error: {response_auto_servicio.text}"
		data = response_auto_servicio.json()
		auto_servicio_id = data.get("Id")
		assert isinstance(auto_servicio_id, int)
		
		# 6. Verificar que se guardó
		db_verify = SessionLocal()
		auto_serv_en_bd = db_verify.query(UsuarioVehiculoServicio).filter(
			UsuarioVehiculoServicio.Id == auto_servicio_id
		).first()
		db_verify.close()
		
		assert auto_serv_en_bd is not None, "El servicio de auto NO se guardó en la BD"
		assert auto_serv_en_bd.usuario_Id == usuario_id
		assert auto_serv_en_bd.vehiculo_Id == vehiculo_id
		assert auto_serv_en_bd.servicio_Id == servicio_id
		
	finally:
		try:
			db.close()
		except:
			pass


def test_listar_servicios_auto():
	"""Test para listar servicios de autos"""
	client = TestClient(app)
	
	# GET debe retornar lista 
	response = client.get("/usuario_vehiculo_servicio/")
	
	assert response.status_code == 200, f"Error: {response.text}"
	data = response.json()
	assert isinstance(data, list), "Se esperaba una lista"
