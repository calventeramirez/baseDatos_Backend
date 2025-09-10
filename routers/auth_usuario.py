from os import access

from fastapi import APIRouter, HTTPException, status
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.params import Depends
from jwt.exceptions import PyJWTError
from passlib.context import CryptContext
from db.client import db_client
from db.models.usuario import Usuario
from datetime import datetime, timedelta, timezone
import os

# Configuración desde variables de entorno
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY", "3228f0d3b5d04c88d2818a85846c2f8c78437f1d2411ec163a9b9eaa04bb6871")

router = APIRouter(
    tags=["Auth"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "No encontrado"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def search_user(username: str) -> Usuario | None:
    """Busca un usuario en la base de datos por username."""
    try:
        user_data = db_client.usuarios.find_one({"username": username})
        print(user_data, username)
        if user_data:
            user_data["id"] = str(user_data["_id"])
            del user_data["_id"]
            return Usuario(**user_data)
        return None
    except Exception as e:
        # Log del error si tienes logging configurado
        print(f"\n\nError buscando usuario: {e}")
        return None

def check_si_primer_setup() -> bool:
    """Verifica si es el primer setup y  no hay usuarios en la bbdd"""
    try:
        user_count = db_client.usuarios.count_documents({})
        return user_count == 0
    except Exception as e:
        print(f"\n\nError buscando usuario: {e}")
        return False

@router.get("/estado")
async def get_setup_status():
    try:
        necesita_setup = check_si_primer_setup()
        return {
            "necesita_setup": necesita_setup,
            "message":"Primer setup requerido" if necesita_setup else "Setup completado"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking setup status: {str(e)}"
        )

@router.post("/primerSetup")
async def primerSetup(datos: Usuario):
    try:
        if not check_si_primer_setup():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El setup inicial ya fue completado. No se permiten más registros."
            )

        hashed_password = crypt.hash(datos.password)

        new_usuario =  {
            "username": datos.username,
            "password": hashed_password
        }

        result = db_client.usuarios.insert_one(new_usuario)

        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear el usuario"
            )

        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token_data= {
            "sub": datos.username,
            "exp": expire,
            "iat": datetime.now(timezone.utc)  # "issued at"
        }

        access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {
            "access_token": access_token,
            "usuario": {
                "id": str(datos.id),
                "username": datos.username
            },
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # en segundos
            "message": "Setup inicial completado. Usuario administrador creado."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el setup inicial: {str(e)}"
        )


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """Autentica un usuario y devuelve un token JWT."""

    # Buscar usuario
    user = search_user(form.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Verificar contraseña
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password incorrecto",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Crear token
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token_data = {
        "sub": user.username,  # "sub" es el estándar JWT para el sujeto
        "exp": expires,
        "iat": datetime.now(timezone.utc)  # "issued at"
    }

    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "usuario": {
            "id": str(user.id),
            "username": user.username
        },
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # en segundos
    }

@router.post("/miusuario")
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Usuario:
    """Obtiene el usuario actual desde el token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = search_user(username)
    if user is None:
        raise credentials_exception

    return user