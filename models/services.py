'''Este archivo define el modelo de servicios en la base de datos'''
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship 
from config.db import Base

class Service(Base):
    '''Modelo para la tabla de servicios'''
    __tablename__ = "tbc_servicios"
    id = Column(Integer, primary_key=True, index=True)
    precio = Column(Float, nullable=False)
    status = Column(Boolean, default=True)
    descripcion = Column(String(255), nullable=True)
    nombreServicio = Column(String(100), unique=True, index=True, nullable=False)
    UserID = Column(Integer, ForeignKey("tbc_usuarios.id"))  # Llave foránea a la tabla de usuarios     