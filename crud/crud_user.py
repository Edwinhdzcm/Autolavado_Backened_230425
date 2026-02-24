import models.auto_servicio as model_auto_servicio
import models.user as model_user
import schemas.schema_user as schema_user
from sqlalchemy.orm import Session
from datetime import datetime

def get_auto_servicio(db: Session, skip: int = 0, limit: int = 100):
    '''Función para obtener los autos de servicio'''
    return db.query(model_auto_servicio.AutoServicio).offset(skip).limit(limit).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Obtener todos los usuarios"""
    return db.query(model_user.User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    """Obtener usuario por ID"""
    return db.query(model_user.User).filter(model_user.User.id == user_id).first()

def get_user_by_email(db: Session, correo_electronico: str):
    """Obtener usuario por email"""
    return db.query(model_user.User).filter(model_user.User.correo_electronico == correo_electronico).first()

def get_user_by_phone(db: Session, numero_telefono: str):
    """Obtener usuario por teléfono"""
    return db.query(model_user.User).filter(model_user.User.numero_telefono == numero_telefono).first()

def create_user(db: Session, user: schema_user.UserCreate):
    """Crear usuario"""

    new_user = model_user.User(
        rol_id=user.Rol_id,
        nombre=user.nombre,
        primer_apellido=user.primer_apellido,
        segundo_apellido=user.segundo_apellido,
        direccion=user.direccion,
        correo_electronico=user.correo_electronico,
        numero_telefono=user.numero_telefono,
        contrasena=user.contrasena,
        estatus=user.estatus if user.estatus is not None else True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def update_user(db: Session, user_id: int, user: schema_user.UserUpdate):
    """Actualizar usuario"""

    db_user = db.query(model_user.User).filter(model_user.User.id == user_id).first()

    if not db_user:
        return None

    db_user.rol_id = user.Rol_id
    db_user.nombre = user.nombre
    db_user.primer_apellido = user.primer_apellido
    db_user.segundo_apellido = user.segundo_apellido
    db_user.direccion = user.direccion
    db_user.correo_electronico = user.correo_electronico
    db_user.numero_telefono = user.numero_telefono
    db_user.contrasena = user.contrasena
    db_user.estatus = user.estatus
    db_user.fecha_actualizacion = datetime.now()

    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db: Session, user_id: int):
    """Eliminar usuario"""

    db_user = db.query(model_user.User).filter(model_user.User.id == user_id).first()

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()

    return db_user