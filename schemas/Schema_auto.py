'''
Docstring for schemas.schema_auto
'''

from pydantic import BaseModel
from datetime import datetime

class AutoBase(BaseModel):
    '''Esquema para el modelo de auto'''
    nombre :str
    user_id:int
    modelo:str
    placa:str
    serie:str
    color:str
    tipo:str
    anio:int
    estado:bool = True
    fecha_registro:datetime
    fecha_actualizacion:datetime
    marca : str

class AutoCreate(AutoBase):
    '''Esquema para crear un nuevo autpo'''
    pass
class AutoUpdate(AutoBase):
    '''Esquema para actualizar un auto existente'''
    pass
class Auto(AutoBase):
    '''Esquema para representar un auto en la base de datos'''
    id: int

    class Config:
        orm_mode = True 