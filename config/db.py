"""Establece la conexión con el servidor de Base de Datos"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Obtener la ruta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar el .env desde la raíz
load_dotenv(BASE_DIR / ".env")

# Soporta ambas convenciones de nombre: `SQLALCHEMY_DATABASE_URL` o `DATABASE_URL`
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL") or os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("No se encontró la variable SQLALCHEMY_DATABASE_URL ni DATABASE_URL en el archivo .env")

# Crear el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base para los modelos
Base = declarative_base()

# --- FUNCIÓN AGREGADA (La que faltaba) ---
def get_db():
    """Crea una nueva sesión de base de datos para cada solicitud y la cierra al finalizar"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()