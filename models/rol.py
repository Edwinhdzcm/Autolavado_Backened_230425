'Estra clase permite generar el modelo para los tipos de rol'

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Date
from sqlalchemy.orm import relationship
from config.db import Base


class rol(Base):
    'Clase para especificar tabla roles de usuario' 
    __tablename__ = "tbc_roles"

    Id = Column(Interger, primary_key=True, index=True)
    nombreRol = column(String(15))
    Estado = column(Boolean)


