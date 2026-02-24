'''
Docstring for schemas.schema_ervices
'''

from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import ConfigDict


class ServicioBase(BaseModel):
    '''Esquema para Servicio (coincide con el modelo SQLAlchemy)'''
    nombre: str
    descripcion: str
    costo: float
    duracion: int = Field(..., alias="duracion_minutos")
    estado: bool = True
    fecha_registro: datetime | None = None
    fecha_actualizacion: datetime | None = None


class ServicioCreate(ServicioBase):
    '''Esquema para crear un nuevo servicio (fecha y id opcionales)'''
    pass


class ServicioUpdate(BaseModel):
    '''Esquema para actualizar un servicio existente (todos opcionales)'''
    nombre: str | None = None
    descripcion: str | None = None
    costo: float | None = None
    duracion: int | None = None
    estado: bool | None = None
    fecha_registro: datetime | None = None
    fecha_actualizacion: datetime | None = None


class Servicio(ServicioBase):
    '''Esquema para representar un servicio en la base de datos'''
    Id: int
    # Allow mapping from SQLAlchemy attribute `duracion_minutos` to `duracion`
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)