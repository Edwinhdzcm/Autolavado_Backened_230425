'Estra clase permite generar el modelo para los tipos de rol'

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Date
from sqlalchemy.orm import relationship
from config.db import Base

class user(Base):
    'clase para especificar tabla de usuarios'
    __tablename__ = "tbb_usuarios"
    Persona_Id = column(Integer, primary_key=True, index=True)
    Rol_Id = column 