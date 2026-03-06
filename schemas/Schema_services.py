from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ServicioBase(BaseModel):
    nombre: str
    descripcion: str
    costo: float
    duracion_minutos: int
    estado: bool = True
    fecha_registro: datetime | None = None
    fecha_actualizacion: datetime | None = None

class ServicioCreate(ServicioBase):
    pass

class ServicioUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    costo: float | None = None
    duracion_minutos: int | None = None
    estado: bool | None = None
    fecha_registro: datetime | None = None
    fecha_actualizacion: datetime | None = None

class Servicio(ServicioBase):
    Id: int
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)