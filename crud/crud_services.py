from sqlalchemy.orm import Session
import models.model_services as model_services


def get_servicios(db: Session, skip: int = 0, limit: int = 100):
    """Devuelve la lista de servicios."""
    return db.query(model_services.Servicios).offset(skip).limit(limit).all()


def get_servicio(db: Session, id: int):
    """Devuelve un servicio por id."""
    return db.query(model_services.Servicios).filter(model_services.Servicios.Id == id).first()


def create_servicio(db: Session, servicio):
    """Crea un nuevo servicio usando un schema Pydantic."""
    # Soportar ambos nombres de campo en el schema: `duracion` o `duracion_minutos`
    duracion_val = getattr(servicio, "duracion_minutos", None)
    if duracion_val is None:
        duracion_val = getattr(servicio, "duracion", None)

    db_servicio = model_services.Servicios(
        nombre=getattr(servicio, "nombre", None),
        descripcion=getattr(servicio, "descripcion", None),
        costo=getattr(servicio, "costo", None),
        duracion_minutos=duracion_val,
        estado=getattr(servicio, "estado", None),
        fecha_registro=getattr(servicio, "fecha_registro", None),
        fecha_actualizacion=getattr(servicio, "fecha_actualizacion", None),
    )
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio


def update_servicio(db: Session, id: int, servicio):
    """Actualiza un servicio existente; devuelve None si no existe."""
    db_obj = get_servicio(db=db, id=id)
    if not db_obj:
        return None

    # soporta Pydantic V2/V1: usar model_dump si existe
    try:
        update_data = servicio.model_dump(exclude_unset=True)
    except Exception:
        update_data = servicio.__dict__

    # Aceptar tanto 'duracion' como 'duracion_minutos' en el payload de actualización
    if "duracion" in update_data:
        update_data["duracion_minutos"] = update_data.pop("duracion")

    for key, value in update_data.items():
        if hasattr(db_obj, key):
            setattr(db_obj, key, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_servicio(db: Session, id: int):
    """Elimina un servicio por id; devuelve el objeto eliminado o None."""
    db_obj = get_servicio(db=db, id=id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj