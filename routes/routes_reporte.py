from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db
import models.model_usuario
import models.model_auto
import models.model_services
from typing import Optional

reporte = APIRouter()

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@reporte.get("/reporte/servicio", tags=["Reportes"])
async def get_reporte_servicio(
    cliente_id: int,
    vehiculo_id: int,
    servicio_id: int,
    operativo_id: int,
    cajero_id: int,
    descuento: float = 0.0,
    db: Session = Depends(get_db)
):
    # Fetch Cliente
    cliente = db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.Id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Fetch Vehiculo
    vehiculo = db.query(models.model_auto.Vehiculo).filter(models.model_auto.Vehiculo.Id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    # Fetch Servicio
    servicio = db.query(models.model_services.Servicio).filter(models.model_services.Servicio.Id == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    # Fetch Operativo
    operativo = db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.Id == operativo_id).first()
    if not operativo:
        raise HTTPException(status_code=404, detail="Operativo no encontrado")

    # Fetch Cajero
    cajero = db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.Id == cajero_id).first()
    if not cajero:
        raise HTTPException(status_code=404, detail="Cajero no encontrado")

    costo_original = servicio.costo if servicio.costo else 0.0
    total = max(0.0, costo_original - descuento)

    reporte_json = {
        "cliente": {
            "id": cliente.Id,
            "nombre_completo": f"{cliente.nombre} {cliente.primer_apellido} {cliente.segundo_apellido}".strip(),
            "correo": cliente.correo_electronico,
            "telefono": cliente.numero_telefono
        },
        "vehiculo": {
            "id": vehiculo.Id,
            "placa": vehiculo.placa,
            "marca": vehiculo.marca,
            "modelo": vehiculo.modelo,
            "color": vehiculo.color
        },
        "servicio": {
            "id": servicio.Id,
            "nombre": servicio.nombre,
            "duracion_minutos": servicio.duracion_minutos
        },
        "personal": {
            "operativo": f"{operativo.nombre} {operativo.primer_apellido}".strip(),
            "cajero": f"{cajero.nombre} {cajero.primer_apellido}".strip()
        },
        "finanzas": {
            "subtotal": costo_original,
            "descuento_aplicado": descuento,
            "total_a_pagar": total
        }
    }

    return reporte_json
