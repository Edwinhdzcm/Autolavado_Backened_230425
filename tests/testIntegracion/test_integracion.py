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

def test_flujo_completo_integracion_red():
    """
    Prueba de Integración End-to-End:
    1. Base -> Rol Creado (vía SQLAlchemy para setup)
    2. API -> Registrar Usuario
    3. API -> Login (Petición de Token)
    4. API -> Protegida -> Crear Auto
    5. API -> Protegida -> Crear Servicio
    6. API -> Protegida -> Crear Relación Auto-Servicio
    """
    db = SessionLocal()
    
    # ==========================
    # 1. SETUP DE ROL BASE
    # ==========================
    rol = Rol(
        nombre_rol=f"InR_{uuid.uuid4().hex[:4]}",
        estado=True,
        fecha_registro=datetime.datetime.now(datetime.timezone.utc),
        fecha_actualizacion=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(rol)
    db.commit()
    db.refresh(rol)
    rol_id = rol.Id
    db.close()
    
    # ==========================
    # 2. REGISTRAR USUARIO (API)
    # ==========================
    nombre = f"usr_int_{uuid.uuid4().hex[:4]}"
    correo = f"{nombre}@flujo.com"
    password = "FlujoIntegracion123"
    
    user_payload = {
        "rol_Id": rol_id,
        "nombre": nombre,
        "primer_apellido": "Int",
        "segundo_apellido": "Full",
        "direccion": "Av. Flujo 123",
        "correo_electronico": correo,
        "numero_telefono": f"99{uuid.uuid4().hex[:4]}",
        "contrasena": password,
        "estado": True,
        "fecha_registro": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "fecha_actualizacion": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    reg_res = client.post("/usuario/", json=user_payload)
    assert reg_res.status_code == 200, f"Error al registrar usuario: {reg_res.text}"
    usuario_id = reg_res.json()["Id"]
    
    # ==========================
    # 3. LOGIN (API)
    # ==========================
    login_res = client.post("/login", data={"username": correo, "password": password})
    assert login_res.status_code == 200, "Error en Login"
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # ==========================
    # 4. CREAR AUTO (API Protegida)
    # ==========================
    auto_placa = f"I{uuid.uuid4().hex[:4].upper()}"
    auto_payload = {
        "usuario_Id": usuario_id,
        "placa": auto_placa,
        "marca": "Tesla",
        "modelo": "Model 3",
        "serie": "T3",
        "color": "Blanco",
        "tipo": "Sedán",
        "anio": 2023,
        "estado": True
    }
    auto_res = client.post("/autos/", json=auto_payload, headers=headers)
    assert auto_res.status_code == 200, f"Error creando Auto: {auto_res.text}"
    auto_id = auto_res.json()["Id"]
    
    # ==========================
    # 5. CREAR SERVICIO (API Protegida)
    # ==========================
    servicio_payload = {
        "nombre": f"ServicioInt_{uuid.uuid4().hex[:4]}",
        "descripcion": "Servicio de prueba de integracion",
        "costo": 50.0,
        "duracion_minutos": 45,
        "estado": True
    }
    serv_res = client.post("/servicio/", json=servicio_payload, headers=headers)
    assert serv_res.status_code == 201, f"Error creando Servicio: {serv_res.text}"
    servicio_id = serv_res.json()["Id"]
    
    # ==========================
    # 6. ASOCIAR AUTO Y SERVICIO
    # ==========================
    auto_serv_payload = {
        "vehiculo_Id": auto_id,
        "cajero_Id": usuario_id,
        "operativo_Id": usuario_id,
        "servicio_Id": servicio_id,
        "fecha": "2023-11-01",
        "hora": "14:30:00",
        "estatus": "Programado",
        "estado": True,
        "fecha_registro": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "fecha_actualizacion": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    rel_res = client.post("/auto-servicio/", json=auto_serv_payload, headers=headers)
    assert rel_res.status_code == 201, f"Error asociando auto-servicio: {rel_res.text}"
    rel_id = rel_res.json()["Id"]
    
    # ==========================
    # VALIDACIÓN FINAL
    # ==========================
    # Si todo llegó hasta aquí, el ciclo de vida completo del negocio funciona a través de HTTP
    assert rel_id > 0
    
    # Se omitió la eliminación porque requieres que los registros se guarden.
