'''Este archivo define el modelo de auto en la base de datos'''
from sqlalchemy import Column, Integer, String, Boolean, Float
from config.db import Base

class Auto(Base):
    '''Modelo para la tabla de autos'''
    __tablename__ = "tbc_autos"
    id = Column(Integer, primary_key=True, index=True)
    modelo = Column(String(50), nullable=False)
    matriucla = Column(String(20), unique=True, index=True, nullable=False)
    marca = Column(String(50), nullable=False)
    color = Column(String(30), nullable=False)
    status = Column(Boolean, default=True)
    clienteID = Column(Integer, nullable=False)