from datetime import datetime, date, time
from pydantic import BaseModel, ConfigDict
from typing import Optional

class AutoServicioBase(BaseModel):
    '''Clase base para modelar los campos de la tabla tbd_usuario_vehiculo_servicio'''
    vehiculo_Id: int
    cajero_Id: int
    operativo_Id: int
    servicio_Id: int
    fecha: date
    hora: time
    estatus: str
    estado: bool = True
    fecha_registro: datetime
    fecha_actualizacion: datetime

class ServicioCreate(AutoServicioBase):
    pass

class ServicioUpdate(AutoServicioBase):
    pass

class Servicio(AutoServicioBase):
    Id: int
    model_config = ConfigDict(from_attributes=True)