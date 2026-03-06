from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from config.db import Base
from datetime import datetime

class Producto(Base):
    __tablename__ = "tbc_productos"

    Id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    categoria = Column(String(50), nullable=True)
    unidad_medida = Column(String(20), nullable=True)
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=0)
    precio = Column(Float, nullable=False)
    estado = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
