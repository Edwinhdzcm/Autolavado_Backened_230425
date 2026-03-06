import uuid
import datetime
import pytest
from sqlalchemy import text
from config.db import SessionLocal
from models.model_rol import Rol
import models.model_usuario
import models.model_auto
import models.model_services
import models.model_auto_servicio

def test_conexion_db():
    """Verifica que la conexión a la base de datos se establezca correctamente usando SQLAlchemy"""
    db = SessionLocal()
    try:
        # Ejecutar un simple SELECT 1 para probar la conexión
        result = db.execute(text("SELECT 1")).scalar()
        assert result == 1, "La conexión a la base de datos falló o no retornó 1"
    finally:
        db.close()

def test_crud_rol_directo():
    """Verifica operaciones CRUD básicas a nivel de base de datos sin usar la API"""
    db = SessionLocal()
    rol_id = None
    try:
        # CREATE
        nombre_unico = f"DBR_{uuid.uuid4().hex[:4]}"
        nuevo_rol = Rol(
            nombre_rol=nombre_unico,
            estado=True,
            fecha_registro=datetime.datetime.now(datetime.timezone.utc),
            fecha_actualizacion=datetime.datetime.now(datetime.timezone.utc)
        )
        db.add(nuevo_rol)
        db.commit()
        db.refresh(nuevo_rol)
        
        rol_id = nuevo_rol.Id
        assert rol_id is not None, "El ID del rol no debería ser nulo si se guardó en BD"
        
        # READ
        rol_leido = db.query(Rol).filter(Rol.Id == rol_id).first()
        assert rol_leido is not None
        assert rol_leido.nombre_rol == nombre_unico
        
        # UPDATE
        nuevo_nombre = f"UR_{uuid.uuid4().hex[:4]}"
        rol_leido.nombre_rol = nuevo_nombre
        db.commit()
        db.refresh(rol_leido)
        
        rol_actualizado = db.query(Rol).filter(Rol.Id == rol_id).first()
        assert rol_actualizado.nombre_rol == nuevo_nombre
        
    finally:
        # DELETE (Limpiar para no dejar basura de este test)
        if rol_id:
            rol_a_borrar = db.query(Rol).filter(Rol.Id == rol_id).first()
            if rol_a_borrar:
                db.delete(rol_a_borrar)
                db.commit()
        db.close()
