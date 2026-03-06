from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from config.db import Base
from datetime import datetime

class Servicio(Base):
    __tablename__ = "tbc_servicios"

    Id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60), nullable=True)                # coincide con MySQL
    descripcion = Column(String(150), nullable=True)
    costo = Column(Float, nullable=True)                      # antes era precio
    duracion_minutos = Column(Integer, nullable=True)         # antes era tiempo_estimado
    estado = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)