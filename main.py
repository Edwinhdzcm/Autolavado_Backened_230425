from fastapi import FastAPI
from config.db import engine, Base

# 1. IMPORT MODELS (Cleaned up duplicates)
from models.model_auto import Vehiculo
import models.model_rol
import models.model_usuario
import models.model_services
import models.model_auto_servicio
import models.model_producto
import models.model_movimiento_inventario

# 2. IMPORT ROUTERS
from routes.routes_rol import rol
from routes.routes_usuario import usuario
from routes.routes_services import services
from routes.routes_auto_servicio import auto_servicio
from routes.routes_auto import auto  # <--- Added this import
from routes.routes_producto import producto
from routes.routes_movimiento_inventario import movimiento_inventario
from routes.routes_reporte import reporte

app = FastAPI(
    title="API  - AutolavadoBackend_230425",
    description=" Alumno : Edwin Hernández Campos"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# 3. INCLUDE ROUTERS
app.include_router(rol)
app.include_router(usuario)
app.include_router(services)
app.include_router(auto_servicio)
app.include_router(auto)
app.include_router(producto)
app.include_router(movimiento_inventario)
app.include_router(reporte)