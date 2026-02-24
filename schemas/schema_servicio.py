'''
Docstring for schemas.schema_servicio
'''
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict

class ServicioBase(BaseModel):
    '''Clase para modelar los campos de tabla Servicios'''
    nombre: str
    descripcion: str
    costo: float
    duaracion_minutos: int
    estado: bool
    fecha_registro: datetime
    fecha_actualizacion: datetime
# pylint: disable=too-few-public-methods, unnecessary-pass
class ServicioCreate(ServicioBase):
    '''Clase para crear un Servicio basado en la tabla Servicios'''
    pass
class ServicioUpdate(ServicioBase):
    '''Clase para actualizar un Servicio basado en la tabla Servicios'''
    pass

class Servicio(ServicioBase):
    '''Clase para realizar operaciones por ID en tabla Servicios'''
    Id: int
    class Config:
        '''Utilizar el orm para ejecutar las funcionalidades'''
        model_config = ConfigDict(from_attributes=True)