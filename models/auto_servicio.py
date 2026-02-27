'''Este archivo define el modelo de auto_servicio en la base de datos'''

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,DateTime
from enum import Enum
from sqlalchemy.orm import relationship 
from config.db import Base

class Estatus (Enum):
    Programando="Programando"
    Proceso="En Proceso"
    Realizado="Realizado"

class AutoServicio(Base):
    '''Modelo para la tabla de auto_servicio'''
    __tablename__ = "tbd_auto_servicio"
    id = Column(Integer, primary_key=True, index=True)
    auto_id=Column (Integer, ForeignKey("tbb_autos.autoid"))
    cajero_id= Column(Integer, ForeignKey("tbb_usuarios.id"))
    operador_id= Column(Integer, ForeignKey("tbb_usuarios.id"))
    servicio_id= Column(Integer, ForeignKey("tbc_servicios.id"))
    fecha= Column(DateTime)
    estatus= Column(String(20), default=Estatus.Programando.value)
    estado= Column(Boolean, default=True)
    fecha_registro= Column(DateTime)
    fecha_actualizacion= Column(DateTime)
