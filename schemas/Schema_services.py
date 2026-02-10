'''
Docstring for schemas.schema_ervices
'''

from pydantic import BaseModel
from datetime import datetime

class ServicioBase(BaseModel):
    '''Esquema para Servicio'''
    nombre: str
    descripcion: str
    costo: float
    duracion: int
    estado: bool
    fecha_registro:datetime
    fecha_actualizacion:datetime


class ServicioCreate(ServicioBase):
    '''Esquema para crear un nuevo servicio'''
    pass
class ServicioUpdate(ServicioBase):
    '''Esquema para actualizar un servicio existente'''
    pass
class Servicio(ServicioBase):
    '''Esquema para representar un servicio en la base de datos'''
    id: int

    class Config:
        orm_mode = True