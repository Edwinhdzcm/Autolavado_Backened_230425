from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from config.db import get_db
from schemas import schema_services
from crud import crud_services
import auth

services = APIRouter()

# GET todos los servicios
@services.get("/servicio/", 
              response_model=List[schema_services.Servicio], 
              tags=["Servicios"])
def read_servicios(skip: int = 0, 
                   limit: int = 100, 
                   db: Session = Depends(get_db),
                   current_user: str = Depends(auth.get_current_user)):
    servicios = crud_services.get_servicios(db=db, skip=skip, limit=limit)
    return servicios

# GET un servicio por ID
@services.get("/servicio/{id}", 
              response_model=schema_services.Servicio, 
              tags=["Servicios"])
def read_servicio(id: int, 
                  db: Session = Depends(get_db),
                  current_user: str = Depends(auth.get_current_user)):
    servicio_db = crud_services.get_servicio(db=db, id=id)
    if servicio_db is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio_db

# POST crear un servicio
@services.post("/servicio/", 
               response_model=schema_services.Servicio, 
               status_code=status.HTTP_201_CREATED,
               tags=["Servicios"])
def create_servicio(servicio: schema_services.ServicioCreate, 
                    db: Session = Depends(get_db),
                    current_user: str = Depends(auth.get_current_user)):
    return crud_services.create_servicio(db=db, servicio=servicio)

# PUT actualizar un servicio
@services.put("/servicio/{id}", 
              response_model=schema_services.Servicio, 
              tags=["Servicios"])
def update_servicio(id: int, 
                    servicio: schema_services.ServicioUpdate, 
                    db: Session = Depends(get_db),
                    current_user: str = Depends(auth.get_current_user)):
    servicio_actualizado = crud_services.update_servicio(db=db, id=id, servicio=servicio)
    if servicio_actualizado is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio_actualizado

# DELETE un servicio
@services.delete("/servicio/{id}", 
                 response_model=schema_services.Servicio, 
                 tags=["Servicios"])
def delete_servicio(id: int, 
                    db: Session = Depends(get_db),
                    current_user: str = Depends(auth.get_current_user)):
    servicio_eliminado = crud_services.delete_servicio(db=db, id=id)
    if servicio_eliminado is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio_eliminado