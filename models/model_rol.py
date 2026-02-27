from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from config.db import Base

class Rol(Base):
    __tablename__ = "tbc_roles"

    Id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(15))
    estado = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_actualizacion = Column(DateTime)

    usuarios = relationship("Usuario", back_populates="rols")