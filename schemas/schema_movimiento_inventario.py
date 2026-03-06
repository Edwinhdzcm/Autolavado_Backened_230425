from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MovimientoInventarioBase(BaseModel):
    Id_producto: int
    Tipo_movimiento: str # 'Entrada' or 'Salida'
    Cantidad: float
    Fecha_movimiento: datetime
    id_usuario: int

class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass

class MovimientoInventarioUpdate(MovimientoInventarioBase):
    pass

class MovimientoInventario(MovimientoInventarioBase):
    Id: int

    model_config = ConfigDict(from_attributes=True)
