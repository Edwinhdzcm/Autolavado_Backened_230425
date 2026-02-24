from sqlalchemy.orm import Session
import models.model_auto_servicio as model_auto_servicio
import schemas.schema_auto_servicio as schema_auto_servicio

def get_auto_servicios(db: Session, skip: int = 0, limit: int = 100):
    '''Función para obtener todos los registros de auto_servicio'''
    # IMPORTANTE: Verifica si en tu archivo models_auto_servicio la clase se llama 
    # AutoServicio o UsuarioVehiculoServicio. Aquí asumo que es AutoServicio.
    return db.query(model_auto_servicio.AutoServicio).offset(skip).limit(limit).all()

def get_auto_servicio(db: Session, id: int):
    '''Función para obtener un solo registro por ID'''
    return db.query(model_auto_servicio.AutoServicio).filter(model_auto_servicio.AutoServicio.Id == id).first()

def create_auto_servicio(db: Session, auto_servicio: schema_auto_servicio.UsuarioVehiculoServicioCreate):
    '''Función para insertar un nuevo registro'''
    db_auto_servicio = model_auto_servicio.AutoServicio(
        vehiculo_Id=auto_servicio.vehiculo_Id,
        cajero_Id=auto_servicio.cajero_Id,
        operativo_Id=auto_servicio.operativo_Id,
        servicio_Id=auto_servicio.servicio_Id,
        fecha=auto_servicio.fecha,
        hora=auto_servicio.hora,
        estatus=auto_servicio.estatus,
        estado=auto_servicio.estado,
        fecha_registro=auto_servicio.fecha_registro,
        fecha_actualizacion=auto_servicio.fecha_actualizacion
    )
    db.add(db_auto_servicio)
    db.commit()
    db.refresh(db_auto_servicio)
    return db_auto_servicio

def update_auto_servicio(db: Session, id: int, auto_servicio: schema_auto_servicio.UsuarioVehiculoServicioUpdate):
    '''Función para actualizar un registro existente'''
    db_obj = get_auto_servicio(db, id)
    if db_obj:
        update_data = auto_servicio.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
    return db_obj

def delete_auto_servicio(db: Session, id: int):
    '''Función para eliminar un registro'''
    db_obj = get_auto_servicio(db, id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj