from sqlalchemy.orm import Session
import models.model_producto as model_producto
import schemas.schema_producto as schema_producto

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_producto.Producto).offset(skip).limit(limit).all()

def get_producto(db: Session, id: int):
    return db.query(model_producto.Producto).filter(model_producto.Producto.Id == id).first()

def get_producto_by_nombre(db: Session, nombre: str):
    return db.query(model_producto.Producto).filter(model_producto.Producto.nombre == nombre).first()

def create_producto(db: Session, producto: schema_producto.ProductoCreate):
    db_producto = model_producto.Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, id: int, producto: schema_producto.ProductoUpdate):
    db_producto = db.query(model_producto.Producto).filter(model_producto.Producto.Id == id).first()
    
    if db_producto:
        for var, value in vars(producto).items():
            if value is not None:
                setattr(db_producto, var, value)
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        
    return db_producto

def delete_producto(db: Session, id: int):
    db_producto = db.query(model_producto.Producto).filter(model_producto.Producto.Id == id).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto
