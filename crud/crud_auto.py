from sqlalchemy.orm import Session
import models.model_auto as model_auto
from schemas import schema_auto

def get_auto(db: Session, id: int):
    # Cambio: model_auto.Auto -> model_auto.Vehiculo | .id -> .Id
    return db.query(model_auto.Vehiculo).filter(model_auto.Vehiculo.Id == id).first()

def get_autos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_auto.Vehiculo).offset(skip).limit(limit).all()

def create_auto(db: Session, auto: schema_auto.VehiculoCreate):
    db_auto = model_auto.Vehiculo(
        usuario_Id=auto.usuario_Id, 
        placa=auto.placa,
        modelo=auto.modelo,
        serie=auto.serie,
        color=auto.color,
        tipo=auto.tipo,
        anio=int(auto.anio),
        marca=getattr(auto, 'marca', "Desconocida") or "Desconocida", # Asegura string no nulo
        estado=auto.estado,
        fecha_registro=auto.fecha_registro,
        fecha_actualizacion=auto.fecha_actualizacion
    )
    db.add(db_auto)
    db.commit()
    db.refresh(db_auto)
    return db_auto

def update_auto(db: Session, id: int, auto: schema_auto.VehiculoUpdate):
    db_obj = get_auto(db, id)
    if db_obj:
        update_data = auto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            # Mantenemos consistencia con las mayúsculas del Schema/Modelo
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
    return db_obj

def delete_auto(db: Session, id: int):
    db_obj = get_auto(db, id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj