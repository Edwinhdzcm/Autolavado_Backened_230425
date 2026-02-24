'''
Docstring for schemas.schema_usuario_vehiculo_servicio
'''
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict

class UsuarioVehiculoServicioBase(BaseModel):
    '''Clase para modelar los campos de tabla usuario_vehiculo_servicio'''
    vehiculo_Id: int
    cajero_Id: int
    operativo_Id: int
    servicio_Id: int
    fecha: str
    hora: str
    estatus: str
    estado: bool
    fecha_registro: datetime
    fecha_actualizacion: datetime
# pylint: disable=too-few-public-methods, unnecessary-pass
class UsuarioVehiculoServicioCreate(UsuarioVehiculoServicioBase):
    '''Clase para crear un usuario_vehiculo_servicio basado en la tabla usuario_vehiculo_servicio'''
    pass
class UsuarioVehiculoServicioUpdate(UsuarioVehiculoServicioBase):
    '''Clase para actualizar un usuario_vehiculo_servicio basado en la tabla usuario_vehiculo_servicio'''
    pass

class UsuarioVehiculoServicio(UsuarioVehiculoServicioBase):
    '''Clase para realizar operaciones por ID en tabla usuario_vehiculo_servicio'''
    Id: int
    class Config:
        '''Utilizar el orm para ejecutar las funcionalidades'''
        model_config = ConfigDict(from_attributes=True)