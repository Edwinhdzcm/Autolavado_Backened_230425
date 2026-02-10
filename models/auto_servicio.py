'''Este archivo define el modelo de auto_servicio en la base de datos'''
import decimal
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey,DateTime,Decimal
from sqlalchemy.orm import relationship 
from config.db import Base

class AutoServicio(Base):
    '''Modelo para la tabla de auto_servicio'''
    __tablename__ = "tbc_auto_servicio"
    id = Column(Integer, primary_key=True, index=True)
    AutoID = Column(Integer, ForeignKey("tbc_autos.id"))  # Llave foránea a la tabla de autos
    ServiceID = Column(Integer, ForeignKey("tbc_servicios.id"))  # Llave foránea a la tabla de servicios
    fechaServicio = Column(DateTime, nullable=False)
    usuarioID = Column(Integer, ForeignKey("tbc_usuarios.id"))  # Llave foránea a la tabla de usuarios
    pagado = Column(Boolean, default=False)
    monto = Column(Decimal(10,2), nullable=False)
    aprobado = Column(Boolean, default=False)
    hora=Column(String(10), nullable=False)