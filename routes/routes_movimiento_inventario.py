from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db
import crud.crud_movimiento_inventario
import schemas.schema_movimiento_inventario
import models.model_movimiento_inventario
import auth
from typing import List

movimiento_inventario = APIRouter()

models.model_movimiento_inventario.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@movimiento_inventario.get("/movimientos-inventario/", response_model=List[schemas.schema_movimiento_inventario.MovimientoInventario], tags=["Movimientos de Inventario"])
async def read_movimientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_movimientos = crud.crud_movimiento_inventario.get_movimientos(db=db, skip=skip, limit=limit)
    return db_movimientos

@movimiento_inventario.get("/movimientos-inventario/{id}", response_model=schemas.schema_movimiento_inventario.MovimientoInventario, tags=["Movimientos de Inventario"])
async def read_movimiento(id: int, db: Session = Depends(get_db)):
    db_movimiento = crud.crud_movimiento_inventario.get_movimiento(db=db, id=id)
    if db_movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return db_movimiento

@movimiento_inventario.post("/movimientos-inventario/", response_model=schemas.schema_movimiento_inventario.MovimientoInventario, tags=["Movimientos de Inventario"])
async def create_movimiento(movimiento: schemas.schema_movimiento_inventario.MovimientoInventarioCreate, db: Session = Depends(get_db)):
    return crud.crud_movimiento_inventario.create_movimiento(db=db, movimiento=movimiento)

@movimiento_inventario.delete("/movimientos-inventario/{id}", response_model=schemas.schema_movimiento_inventario.MovimientoInventario, tags=["Movimientos de Inventario"])
async def delete_movimiento(id: int, db: Session = Depends(get_db)):
    db_movimiento = crud.crud_movimiento_inventario.delete_movimiento(db=db, id=id)
    if db_movimiento is None:
        raise HTTPException(status_code=404, detail="El movimiento no existe, no se pudo eliminar")
    return db_movimiento
