'''Este archivo define el modelo de servicios en la base de datos'''
from sqlalchemy import Column, Integer, String, Boolean, Float,DateTime
from sqlalchemy.orm import relationship 
from config.db import Base

class Service(Base):
    '''Modelo para la tabla de servicios'''
    __tablename__ = "tbc_servicios"
    id = Column(Integer, primary_key=True, index=True)
    nombre =Column(String(50))
    descripcion=Column(String(50))
    costo = Column(Float, nullable=False)
    duracion = Column(Integer, nullable=False)
    estado = Column(Boolean, default=True)
    fecha_registro = Column(DateTime)
    fecha_actualizacion = Column(DateTime)