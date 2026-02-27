from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import auth

from config.db import get_db
from crud import crud_auto_servicio
from schemas import schema_auto_servicio

auto_servicio = APIRouter()

@auto_servicio.get(
    "/auto-servicio/",
    # CAMBIO: Se cambió AutoServicio por UsuarioVehiculoServicio
    response_model=List[schema_auto_servicio.UsuarioVehiculoServicio], 
    tags=["AutoServicio"]
)
def read_auto_servicios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    return crud_auto_servicio.get_auto_servicios(db=db, skip=skip, limit=limit)


@auto_servicio.get(
    "/auto-servicio/{id}",
    # CAMBIO: Se cambió AutoServicio por UsuarioVehiculoServicio
    response_model=schema_auto_servicio.UsuarioVehiculoServicio,
    tags=["AutoServicio"]
)
def read_auto_servicio(id: int, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    db_auto_servicio = crud_auto_servicio.get_auto_servicio(db=db, id=id)
    if db_auto_servicio is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return db_auto_servicio


@auto_servicio.post(
    "/auto-servicio/",
    # CAMBIO: Se cambió AutoServicio por UsuarioVehiculoServicio
    response_model=schema_auto_servicio.UsuarioVehiculoServicio,
    status_code=status.HTTP_201_CREATED,
    tags=["AutoServicio"]
)
def create_auto_servicio(
    # CAMBIO: Se cambió AutoServicioCreate por UsuarioVehiculoServicioCreate
    auto_servicio: schema_auto_servicio.UsuarioVehiculoServicioCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    return crud_auto_servicio.create_auto_servicio(db=db, auto_servicio=auto_servicio)


@auto_servicio.put(
    "/auto-servicio/{id}",
    # CAMBIO: Se cambió AutoServicio por UsuarioVehiculoServicio
    response_model=schema_auto_servicio.UsuarioVehiculoServicio,
    tags=["AutoServicio"]
)
def update_auto_servicio(
    id: int,
    # CAMBIO: Se cambió AutoServicioUpdate por UsuarioVehiculoServicioUpdate
    auto_servicio: schema_auto_servicio.UsuarioVehiculoServicioUpdate,
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


@auto_servicio.delete(
    "/auto-servicio/{id}",
    # CAMBIO: Se cambió AutoServicio por UsuarioVehiculoServicio
    response_model=schema_auto_servicio.UsuarioVehiculoServicio,
    tags=["AutoServicio"]
)
def delete_auto_servicio(id: int, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    db_auto_servicio = crud_auto_servicio.delete_auto_servicio(db=db, id=id)
    if db_auto_servicio is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return db_auto_servicio