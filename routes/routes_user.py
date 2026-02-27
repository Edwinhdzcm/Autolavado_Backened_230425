from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import auth

import crud.crud_user as crud_user
import config.db as db_config
import schemas.schema_user as schema_user
import models.user as model_user

user = APIRouter()

pwd_context = model_user.CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear tablas
model_user.Base.metadata.create_all(bind=db_config.engine)


def get_db():
    db = db_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user.get("/usuarios", response_model=List[schema_user.User], tags=["Usuarios"])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    usuarios = crud_user.get_users(db=db, skip=skip, limit=limit)
    return usuarios


@user.get("/usuarios/{user_id}", response_model=schema_user.User, tags=["Usuarios"])
async def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    db_user = crud_user.get_user_by_id(db=db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return db_user


@user.post("/usuarios", response_model=schema_user.User, tags=["Usuarios"])
async def create_user(
    usuario: schema_user.UserCreate,
    db: Session = Depends(get_db)
):
    return crud_user.create_user(db=db, user=usuario)


@user.put("/usuarios/{user_id}", response_model=schema_user.User, tags=["Usuarios"])
async def update_user(
    user_id: int,
    usuario: schema_user.UserUpda,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    db_user = crud_user.update_user(db=db, user_id=user_id, user=usuario)

    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return db_user


@user.delete("/usuarios/{user_id}", tags=["Usuarios"])
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    db_user = crud_user.delete_user(db=db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"message": "Usuario eliminado correctamente"}