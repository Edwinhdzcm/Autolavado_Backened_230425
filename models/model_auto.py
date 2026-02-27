from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from config.db import Base
from datetime import datetime

class Vehiculo(Base):
    __tablename__ = "tbb_vehiculos" # Revisa que este sea el nombre real de tu tabla

    Id = Column(Integer, primary_key=True, index=True) # Debe ser 'id' en minúsculas
    usuario_Id = Column(Integer, ForeignKey("tbb_usuarios.Id")) # FK al usuario
    placa = Column(String(20), unique=True)
    marca = Column(String(50))  # <--- Asegúrate que exista en tu DB
    modelo = Column(String(50))
    serie = Column(String(50))
    color = Column(String(20))
    tipo = Column(String(20))
    anio = Column(String(4))    # <--- Aquí está como String para coincidir con tu Schema
    estado = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)