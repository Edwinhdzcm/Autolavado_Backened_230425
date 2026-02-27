from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import config.db
import crud.crud_usuario
import schemas.schema_usuario
import models.model_usuario
import auth
from typing import List

usuario = APIRouter()

models.model_usuario.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@usuario.get("/usuario/", response_model=List[schemas.schema_usuario.Usuario], tags=["Usuarios"])
async def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    db_usuario= crud.crud_usuario.get_usuario(db=db, skip=skip, limit=limit)
    return db_usuario

@usuario.post("/usuario/", response_model=schemas.schema_usuario.Usuario, tags=["Usuarios"])
def create_usuario(usuario: schemas.schema_usuario.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.crud_usuario.get_usuario_by_nombre(db, nombre=usuario.nombre)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Usuario existente intenta nuevamente")
    return crud.crud_usuario.create_usuario(db=db, usuario=usuario)

@usuario.put("/usuario/{id}", response_model=schemas.schema_usuario.Usuario, tags=["Usuarios"])
async def update_usuario(id: int, usuario: schemas.schema_usuario.UsuarioUpdate, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    db_usuario = crud.crud_usuario.update_usuario(db=db, id=id, usuario=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no existe, no actualizado")
    return db_usuario

@usuario.delete("/usuario/{id}", response_model=schemas.schema_usuario.Usuario, tags=["Usuarios"])
async def delete_usuario(id: int, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    db_usuario = crud.crud_usuario.delete_usuario(db=db, id=id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="El Usuario no existe, no se pudo eliminar")
    return db_usuario

@usuario.post("/login/", tags=["Login"])
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = crud.crud_usuario.authenticate_user(db, form_data.username, form_data.password)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Generamos el token real guardando el ID del usuario en el campo "sub" (subject)
    token_real = auth.create_access_token(data={"sub": str(usuario.Id)})
    
    return {"access_token": token_real, "token_type": "bearer"}