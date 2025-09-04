from pydantic import  BaseModel

class Videos(BaseModel):
    id: str | None
    tituloEsp: str
    tituloOrg: str | None
    tematica: str
    director: str
    protagonistas: str
    companiaCinematografica: str
    duracion: int
    idiomasAudios: str
    idiomasSubtitulos: str
    formato: str
    pais: str
    nacionalidad: str
    portada: str | None
    argumento: str