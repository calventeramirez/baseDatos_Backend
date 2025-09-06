from pydantic import  BaseModel

class CDROM(BaseModel):
    id: str | None
    titulo: str
    tematica: str
    duracion: float | None
    yearGrab: int
    coleccion: str | None