from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import crud.crud_rol
import config.db
import schemas.schema_rol
import models.model_rol
import auth
from typing import List

rol = APIRouter()

models.model_rol.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@rol.get("/rol/", response_model=List[schemas.schema_rol.Rol], tags=["Roles"])
async def read_rols(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # esta ruta queda pública según la petición del usuario
    db_rol= crud.crud_rol.get_rol(db=db, skip=skip, limit=limit)
    return db_rol


@rol.post("/rol/", response_model=schemas.schema_rol.Rol, tags=["Roles"])
def create_rol(rol: schemas.schema_rol.RolCreate, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    db_rol = crud.crud_rol.get_rol_by_nombre(db, nombre_rol=rol.nombre_rol)
    if db_rol:
        raise HTTPException(status_code=400, detail="Rol existente intenta nuevamente")
    return crud.crud_rol.create_rol(db=db, rol=rol)

@rol.put("/rol/{id}", response_model=schemas.schema_rol.Rol, tags=["Roles"])
async def update_rol(id: int, rol: schemas.schema_rol.RolUpdate, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    db_rol = crud.crud_rol.update_rol(db=db, id=id, rol=rol)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no existe, no actualizado")
    return db_rol

@rol.delete("/rol/{id}", response_model=schemas.schema_rol.Rol, tags=["Roles"])
async def delete_rol(id: int, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    db_rol = crud.crud_rol.delete_rol(db=db, id=id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="El Rol no existe, no se pudo eliminar")
    return db_rol