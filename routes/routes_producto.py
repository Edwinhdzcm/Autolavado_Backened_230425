from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db
import crud.crud_producto
import schemas.schema_producto
import models.model_producto
import auth
from typing import List

producto = APIRouter()

models.model_producto.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@producto.get("/productos/", response_model=List[schemas.schema_producto.Producto], tags=["Productos"])
async def read_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_productos = crud.crud_producto.get_productos(db=db, skip=skip, limit=limit)
    return db_productos

@producto.get("/productos/{id}", response_model=schemas.schema_producto.Producto, tags=["Productos"])
async def read_producto(id: int, db: Session = Depends(get_db)):
    db_producto = crud.crud_producto.get_producto(db=db, id=id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@producto.post("/productos/", response_model=schemas.schema_producto.Producto, tags=["Productos"])
async def create_producto(producto: schemas.schema_producto.ProductoCreate, db: Session = Depends(get_db)):
    # Verify if name already exists to prevent duplicates (optional)
    db_producto = crud.crud_producto.get_producto_by_nombre(db, nombre=producto.nombre)
    if db_producto:
        raise HTTPException(status_code=400, detail="El producto ya existe")
    return crud.crud_producto.create_producto(db=db, producto=producto)

@producto.put("/productos/{id}", response_model=schemas.schema_producto.Producto, tags=["Productos"])
async def update_producto(id: int, producto: schemas.schema_producto.ProductoUpdate, db: Session = Depends(get_db)):
    db_producto = crud.crud_producto.update_producto(db=db, id=id, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no existe, no actualizado")
    return db_producto

@producto.delete("/productos/{id}", response_model=schemas.schema_producto.Producto, tags=["Productos"])
async def delete_producto(id: int, db: Session = Depends(get_db)):
    db_producto = crud.crud_producto.delete_producto(db=db, id=id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="El Producto no existe, no se pudo eliminar")
    return db_producto
