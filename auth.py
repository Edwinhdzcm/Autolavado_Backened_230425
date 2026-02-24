from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

# Configuración de seguridad (Idealmente, SECRET_KEY debería ir en tu archivo .env)
SECRET_KEY = "clave_super_secreta_de_mi_estacionamiento" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # El token durará 30 minutos

# Le indicamos a FastAPI cuál es la ruta exacta donde los usuarios inician sesión
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    
    # Calculamos la fecha y hora exacta en la que el token dejará de servir
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Generamos la cadena de texto encriptada (El JWT)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt