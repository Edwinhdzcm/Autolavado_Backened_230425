from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import auth

# 1. IMPORTACIÓN CORREGIDA: Traemos 'Vehiculo' que es el nombre real en tu modelo
from models.model_auto import Vehiculo as VehiculoModel
from schemas.schema_auto import Vehiculo as VehiculoSchema, VehiculoCreate, VehiculoUpdate 
from config.db import get_db

auto = APIRouter()

@auto.get("/autos/", response_model=List[VehiculoSchema], tags=["Autos"])
def read_autos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    # Usamos VehiculoModel (SQLAlchemy) para la consulta
    autos = db.query(VehiculoModel).offset(skip).limit(limit).all()
    return autos

@auto.get("/autos/{id}", response_model=VehiculoSchema, tags=["Autos"])
def read_auto(id: int, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    # Nota: Tu modelo tiene 'Id' con mayúscula en la base de datos según lo que me mostraste
    db_auto = db.query(VehiculoModel).filter(VehiculoModel.Id == id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_auto

@auto.post("/autos/", response_model=VehiculoSchema, tags=["Autos"])
def create_auto_route(vehiculo: VehiculoCreate, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    db_auto = VehiculoModel(
        usuario_Id=vehiculo.usuario_Id, # Asegúrate que coincida con las mayúsculas de tu modelo
        placa=vehiculo.placa,
        # marca=vehiculo.marca, # Cuidado: 'marca' NO estaba en el modelo que me pasaste
        modelo=vehiculo.modelo,
        serie=vehiculo.serie,
        color=vehiculo.color,
        tipo=vehiculo.tipo,
        anio=str(vehiculo.anio) if vehiculo.anio else None, 
        estado=vehiculo.estado,
        fecha_registro=vehiculo.fecha_registro,
        fecha_actualizacion=vehiculo.fecha_actualizacion
    )
    db.add(db_auto)
    db.commit()
    db.refresh(db_auto)
    return db_auto

@auto.put("/autos/{id}", response_model=VehiculoSchema, tags=["Autos"])
def update_auto_route(id: int, vehiculo: VehiculoUpdate, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    db_obj = db.query(VehiculoModel).filter(VehiculoModel.Id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    update_data = vehiculo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_obj, key, value)
            
    db.commit()
    db.refresh(db_obj)
    return db_obj

@auto.delete("/autos/{id}", tags=["Autos"])
def delete_auto_route(id: int, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    db_obj = db.query(VehiculoModel).filter(VehiculoModel.Id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    db.delete(db_obj)
    db.commit()
    return {"message": f"Vehículo con id {id} eliminado correctamente"}