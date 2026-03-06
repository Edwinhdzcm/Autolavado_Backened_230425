from sqlalchemy.orm import Session
import models.model_movimiento_inventario as model_movimiento
import schemas.schema_movimiento_inventario as schema_movimiento
import models.model_producto as model_producto
from fastapi import HTTPException

def get_movimientos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_movimiento.MovimientoInventario).offset(skip).limit(limit).all()

def get_movimiento(db: Session, id: int):
    return db.query(model_movimiento.MovimientoInventario).filter(model_movimiento.MovimientoInventario.Id == id).first()

def create_movimiento(db: Session, movimiento: schema_movimiento.MovimientoInventarioCreate):
    # Verify product exists
    db_producto = db.query(model_producto.Producto).filter(model_producto.Producto.Id == movimiento.Id_producto).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Update product stock based on movement type
    if movimiento.Tipo_movimiento.lower() == 'entrada':
        db_producto.stock_actual += movimiento.Cantidad
    elif movimiento.Tipo_movimiento.lower() == 'salida':
        if db_producto.stock_actual < movimiento.Cantidad:
            raise HTTPException(status_code=400, detail="Stock insuficiente para la salida")
        db_producto.stock_actual -= movimiento.Cantidad
    else:
        raise HTTPException(status_code=400, detail="Tipo_movimiento debe ser 'Entrada' o 'Salida'")

    db_movimiento = model_movimiento.MovimientoInventario(**movimiento.model_dump())
    db.add(db_movimiento)
    db.add(db_producto)
    db.commit()
    db.refresh(db_movimiento)
    db.refresh(db_producto)
    
    return db_movimiento

def delete_movimiento(db: Session, id: int):
    # Depending on requirements, deleting a movement might need to revert stock.
    # We will just do a standard delete here as keeping history is standard.
    db_movimiento = db.query(model_movimiento.MovimientoInventario).filter(model_movimiento.MovimientoInventario.Id == id).first()
    if db_movimiento:
        db.delete(db_movimiento)
        db.commit()
    return db_movimiento
