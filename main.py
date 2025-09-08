from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import libros, auth_usuario, videos, cdrom, arte, revista, musica

app = FastAPI()

#Permitir origenes
origins = [
    "http://localhost:3000", #front end en local con nextJS
    "http://127.0.0.1:3000"
]

#Añadir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #Origenes permitidos
    allow_credentials=True,
    allow_methods=["*"], # Metodos permitidos (GET, POST, PUT, DELETE)
    allow_headers=["*"], # Headers permitidos
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
