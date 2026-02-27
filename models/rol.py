''''Esta clase permite generar el modelo para los tipos de roles'''
from sqlalchemy import Column, Integer, String, Boolean,Column,DateTime
from config.db import Base

class Rol(Base):
    '''Modelo para la tabla de roles'''
    __tablename__ = "tbc_roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), unique=True, index=True, nullable=False)
    estado = Column(Boolean, default=True)
    fecha_registro= Column(DateTime)
    fecha_modificacion= Column(DateTime)