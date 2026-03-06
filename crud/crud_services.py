from sqlalchemy.orm import Session
from models import model_services
from schemas.schema_auto_servicio import ServicioCreate

def get_servicios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_services.Servicio).offset(skip).limit(limit).all()

def create_servicio(db: Session, servicio: ServicioCreate):
    db_servicio = model_services.Servicio(
        nombre=servicio.nombre,
        descripcion=servicio.descripcion,
        costo=servicio.costo,
        duracion_minutos=servicio.duracion_minutos,
        estado=servicio.estado
    )
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio