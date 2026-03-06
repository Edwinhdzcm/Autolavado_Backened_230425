from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from config.db import Base
from datetime import datetime

class MovimientoInventario(Base):
    __tablename__ = "tbb_movimientos_inventario"

    Id = Column(Integer, primary_key=True, index=True)
    Id_producto = Column(Integer, ForeignKey("tbc_productos.Id"))
    Tipo_movimiento = Column(String(20), nullable=False) # 'Entrada' o 'Salida'
    Cantidad = Column(Float, nullable=False)
    Fecha_movimiento = Column(DateTime, default=datetime.utcnow)
    id_usuario = Column(Integer, ForeignKey("tbb_usuarios.Id"))
