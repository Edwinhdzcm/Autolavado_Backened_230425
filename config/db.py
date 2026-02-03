'Establece la conexion con el servidor de Base de Datos'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://root1234@localhost:3307/autolavadodb"
engine = create_engine (SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker (autocomit=false, autoflush=false, bind=engine)
Base = declarative_base()
