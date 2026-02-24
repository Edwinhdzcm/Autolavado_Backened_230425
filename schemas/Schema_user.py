'''
Docstring for schemas.schema_user
'''

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict

class UserBase(BaseModel):
    '''Esquema base para los usuarios'''
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
    '''Esquema para crear un nuevo usuario'''
    pass
class UserUpdate(UserBase):
    '''Esquema para actualizar un usuario existente'''
    pass
class User(UserBase):
    '''Esquema para representar un usuario en la base de datos'''
    id: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    '''Clase para realizar el login por numero o correo'''
    numero_telefono :Optional [str]= None
    correo_electronico : Optional[str] = None
    contrasena: str
    class Config:
        model_config = ConfigDict(from_attributes=True)