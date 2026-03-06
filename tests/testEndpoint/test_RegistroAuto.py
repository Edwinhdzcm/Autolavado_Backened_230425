import os
import uuid
import datetime
from datetime import timezone
import pytest
from fastapi.testclient import TestClient
from main import app
from config.db import SessionLocal
from models.model_auto import Vehiculo
from models.model_usuario import Usuario
from models.model_rol import Rol
from crud.crud_usuario import pwd_context
import auth

@pytest.fixture(autouse=True)
def override_auth():
    def override_get_current_user():
        return "test_user"
    app.dependency_overrides[auth.get_current_user] = override_get_current_user
    yield
    app.dependency_overrides = {}

def test_crear_auto_exitoso():
    client = TestClient(app)
    db = SessionLocal()
    auto_id_creado = None
    usuario_id = None
    # 1. Crear Rol primero para la foreign key del Usuario
    rol = Rol(
        nombre_rol=f"R_{uuid.uuid4().hex[:4]}",
        estado=True,
        fecha_registro=datetime.datetime.now(timezone.utc),
        fecha_actualizacion=datetime.datetime.now(timezone.utc)
    )
    db.add(rol)
    db.commit()
    db.refresh(rol)
    rol_id = rol.Id

    # 2. Crear Usuario 
    usuario = Usuario(
        rol_Id=rol_id, nombre=f"u_{uuid.uuid4().hex[:4]}", primer_apellido="T", segundo_apellido="A",
        direccion="C", correo_electronico=f"t{uuid.uuid4().hex[:4]}@t.com",
        numero_telefono="1", contrasena=pwd_context.hash("p"), estado=True,
        fecha_registro=datetime.datetime.now(timezone.utc),
        fecha_actualizacion=datetime.datetime.now(timezone.utc)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    usuario_id = usuario.Id

    # 2. Crear Auto asociado a ese Usuario
    payload = {
        "usuario_Id": usuario_id, 
        "placa": f"P{uuid.uuid4().hex[:4].upper()}",
        "marca": "Toyota", 
        "modelo": "Corolla", 
        "serie": "1", 
        "color": "B", 
        "tipo": "S",
        "anio": 2020, 
        "estado": True,
        "fecha_registro": datetime.datetime.now(timezone.utc).isoformat(),
        "fecha_actualizacion": datetime.datetime.now(timezone.utc).isoformat()
    }
    res = client.post("/autos/", json=payload)
    assert res.status_code == 200
    auto_id_creado = res.json().get("Id")


def test_obtener_autos():
    client = TestClient(app)
    res = client.get("/autos/")
    assert res.status_code == 200