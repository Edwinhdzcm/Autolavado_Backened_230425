from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    Rol_id: int
    nombre: str
    primer_apellido: str
    segundo_apellido: str
    direccion: str
    correo_electronico: str
    numero_telefono: str
    contrasena: str
    estatus: bool = True
    fecha_registro: datetime
    fecha_actualizacion: datetime

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    # Corregido: Sintaxis Pydantic V2
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    numero_telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    contrasena: str
    model_config = ConfigDict(from_attributes=True)