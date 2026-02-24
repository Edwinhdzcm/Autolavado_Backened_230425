'''
Docstring for schemas.schema_vehiculo
'''
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict 

class VehiculoBase(BaseModel):
    '''Clase para modelar los campos de tabla Vehiculo'''
    usuario_Id: int
    placa: str
    marca: str 
    modelo: str
    serie: str
    color: str
    tipo: str
    anio: int | str
    estado: bool = True
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

class VehiculoCreate(VehiculoBase):
    '''Clase para crear un Vehiculo basado en la tabla Vehiculo'''
    pass

class VehiculoUpdate(VehiculoBase):
    '''Clase para actualizar un Vehiculo basado en la tabla Vehiculo'''
    usuario_Id: Optional[int] = None
    placa: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    serie: Optional[str] = None
    color: Optional[str] = None
    tipo: Optional[str] = None
    anio: Optional[int | str] = None
    estado: Optional[bool] = None

class Vehiculo(VehiculoBase):
    '''Clase para realizar operaciones por ID en tabla Vehiculo'''
    # CAMBIO IMPORTANTE: 'Id' con mayúscula para coincidir con tu MySQL
    Id: int 

    # Estándar de Pydantic V2
    model_config = ConfigDict(from_attributes=True)