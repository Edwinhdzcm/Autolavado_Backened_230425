# AutolavadoPy_230417

Una API backend ligera para gestionar un sistema de autolavado.

Características principales
- API REST construida con FastAPI
- Documentación interactiva en `/docs`
- Conexión a base de datos via `DATABASE_URL` (MySQL compatible con SQLAlchemy)

Requisitos
- Python 3.10+ (o la versión de tu entorno virtual)
- MySQL o MariaDB en ejecución

Instalación y ejecución (Windows)
1. Abrir terminal en la raíz del proyecto.
2. Crear y activar el entorno virtual:

```powershell
python -m venv entornoBackend
entornoBackend\Scripts\activate
```

3. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

4. Crear el archivo de configuración `.env` en la raíz con la variable de conexión:

```text
DATABASE_URL=mysql+pymysql://root:1234@localhost/autolavado
```

5. Levantar la aplicación (modo desarrollo):

```powershell
uvicorn main:app --reload
```

6. Abrir la documentación interactiva en el navegador:

```
http://127.0.0.1:8000/docs
```