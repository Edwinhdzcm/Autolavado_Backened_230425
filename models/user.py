'''Este archivo define el modelo de usuarios en la base de datos'''
from sqlalchemy import Column, Integer, String, Boolean,DateTime,Enum,Date,ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class User(Base):
    '''Modelo para la tabla de usuarios'''
    __tablename__ = "tbc_usuarios"
    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("tbc_roles.id"))  # Llave foránea a la tabla de roles
    nombre = Column(String(50))
    primer_apellido = Column(String(50))
    segundo_apellido = Column(String(50))
    direccion = Column(String(255))
    correo_electronico = Column(String(100))
    numero_telefono = Column(String(20))
    contrasena=Column(String(100))
    estatus= Column(Boolean, default=True)
    fecha_registro= Column(DateTime)
    fecha_actualizacion=Column(DateTime)
 