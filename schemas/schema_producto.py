from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    unidad_medida: Optional[str] = None
    stock_actual: int = 0
    stock_minimo: int = 0
    precio: float
    estado: bool = True
    fecha_registro: datetime
    fecha_actualizacion: datetime

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

class Producto(ProductoBase):
    Id: int

    model_config = ConfigDict(from_attributes=True)
