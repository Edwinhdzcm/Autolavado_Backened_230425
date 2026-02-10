'''Este archivo define el modelo de cliente en la base de datos'''
from sqlalchemy import Column, Integer, String, Boolean
from config.db import Base  

class Cliente(Base):
    '''Modelo para la tabla de clientes'''
    __tablename__ = "tbc_clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellidoPaterno = Column(String(50), nullable=False)
    apellidoMaterno = Column(String(50), nullable=False)
    telefono = Column(String(15), unique=True, index=True, nullable=False)
    direction = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    telefono = Column(String(15), nullable=True)
    password = Column(String(100), nullable=False)
    status = Column(Boolean, default=True)    