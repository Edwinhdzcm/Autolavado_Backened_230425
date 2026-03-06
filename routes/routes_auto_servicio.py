from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import auth

from config.db import get_db
from crud import crud_auto_servicio
from schemas import schema_auto_servicio

auto_servicio = APIRouter()

# ================= GET TODOS LOS SERVICIOS =================
@auto_servicio.get(
    "/auto-servicio/",
    response_model=List[schema_auto_servicio.Servicio],
    tags=["AutoServicio"]
)
def read_auto_servicios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    return crud_auto_servicio.get_auto_servicios(db=db, skip=skip, limit=limit)


# ================= GET SERVICIO POR ID =================
@auto_servicio.get(
    "/auto-servicio/{id}",
    response_model=schema_auto_servicio.Servicio,
    tags=["AutoServicio"]
)
def read_auto_servicio(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(auth.get_current_user)
):
    db_auto_servicio = crud_auto_servicio.get_auto_servicio(db=db, id=id)
    if db_auto_servicio is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return db_auto_servicio


# ================= CREAR SERVICIO =================
@auto_servicio.post(
    "/auto-servicio/",
    response_model=schema_auto_servicio.Servicio,
    status_code=status.HTTP_201_CREATED,
    tags=["AutoServicio"]
)
def create_auto_servicio(
    auto_servicio: schema_auto_servicio.ServicioCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    return crud_auto_servicio.create_auto_servicio(db=db, auto_servicio=auto_servicio)


# ================= ACTUALIZAR SERVICIO =================
@auto_servicio.put(
    "/auto-servicio/{id}",
    response_model=schema_auto_servicio.Servicio,
    tags=["AutoServicio"]
)
def update_auto_servicio(
    id: int,
    auto_servicio: schema_auto_servicio.ServicioUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    db_auto_servicio = crud_auto_servicio.update_auto_servicio(
        db=db,
        id=id,
        auto_servicio=auto_servicio
    )
    if db_auto_servicio is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return db_auto_servicio


# ================= ELIMINAR SERVICIO =================
@auto_servicio.delete(
    "/auto-servicio/{id}",
    response_model=schema_auto_servicio.Servicio,
    tags=["AutoServicio"]
)
def delete_auto_servicio(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(auth.get_current_user)
):
    db_auto_servicio = crud_auto_servicio.delete_auto_servicio(db=db, id=id)
    if db_auto_servicio is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return db_auto_servicio