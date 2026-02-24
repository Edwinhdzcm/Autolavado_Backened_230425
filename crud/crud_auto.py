from sqlalchemy.orm import Session
import models.model_auto as model_auto
from schemas import schema_auto

def get_auto(db: Session, id: int):
    '''Obtiene un auto específico por su ID (usando id en minúscula del modelo)'''
    return db.query(model_auto.Auto).filter(model_auto.Auto.id == id).first()

def get_autos(db: Session, skip: int = 0, limit: int = 100):
    '''Obtiene la lista de todos los autos registrados en tbb_autos'''
    return db.query(model_auto.Auto).offset(skip).limit(limit).all()

def create_auto(db: Session, auto: schema_auto.VehiculoCreate):
    '''Crea un nuevo registro mapeando schema (Campos con I) a modelo (campos en minúscula)'''
    db_auto = model_auto.Auto(
        usuario_id=auto.usuario_Id, # Mapeo de I mayúscula a i minúscula
        placa=auto.placa,
        modelo=auto.modelo,
        serie=auto.serie,
        color=auto.color,
        tipo=auto.tipo,
        anio=int(auto.anio), # Conversión a entero para el modelo
        marca=getattr(auto, 'marca', "Desconocida"), # Evita error si marca no viene en schema
        estado=auto.estado,
        fecha_registro=auto.fecha_registro,
        fecha_actualizacion=auto.fecha_actualizacion
    )
    db.add(db_auto)
    db.commit()
    db.refresh(db_auto)
    return db_auto

def update_auto(db: Session, id: int, auto: schema_auto.VehiculoUpdate):
    '''Actualiza los datos de un auto existente usando model_dump'''
    db_obj = get_auto(db, id)
    if db_obj:
        # Convertimos el esquema a diccionario para actualizar dinámicamente
        update_data = auto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            # Mapeo manual para campos con diferencias de mayúsculas si es necesario
            if key == "usuario_Id":
                setattr(db_obj, "usuario_id", value)
            else:
                setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
    return db_obj

def delete_auto(db: Session, id: int):
    '''Elimina físicamente el registro de la tabla tbb_autos'''
    db_obj = get_auto(db, id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj