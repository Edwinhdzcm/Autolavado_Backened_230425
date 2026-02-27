from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from config.db import Base

class Servicios(Base):
    __tablename__ = "tbc_servicios"

    Id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60))
    descripcion = Column(String(150))
    costo = Column(Float)
    duracion_minutos = Column(Integer)
    estado = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_actualizacion = Column(DateTime)