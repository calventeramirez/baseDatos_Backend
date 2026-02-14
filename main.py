from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import libros, auth_usuario, videos, cdrom, arte, revista, musica

app = FastAPI()

# Aqui defines los origenes permitidos (frontend)
origins = [
    "http://localhost:3000",  # tu frontend local
    "http://127.0.0.1:3000",  # por si usas esta direccion
    "*",
]

# Activar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],            # permite todos los metodos (GET, POST, etc.)
    allow_headers=["*"],            # permite todos los headers
)

#Routers
app.include_router(arte.router)
app.include_router(cdrom.router)
app.include_router(libros.router)
app.include_router(musica.router)
app.include_router(revista.router)
app.include_router(videos.router)
app.include_router(auth_usuario.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
