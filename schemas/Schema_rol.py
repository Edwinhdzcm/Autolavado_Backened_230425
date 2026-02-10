'''
Docstring for schemas.schema_rol
'''

from pydantic import BaseModel
from datetime import datetime
class RolBase(BaseModel):
    '''Esquema base para los roles'''
    nombre_rol: str
    estado: bool = True
    fecha_registro: datetime
    fecha_actualizacion: datetime

class RolCreate(RolBase):
    '''Esquema para crear un nuevo rol'''
    pass
class RolUpdate(RolBase):
    '''Esquema para actualizar un rol existente'''
    pass
class Rol(RolBase):
    '''Esquema para representar un rol en la base de datos'''
    id: int

    class Config:
        orm_mode = True