from pydantic import  BaseModel

class Revista(BaseModel):
    id: str | None
    titulo: str
    tematica: str
    editorial: str
    fechaEdicion: int | None
    numPag: int | None
    numRevista: int | None
    fotoPortada: str | None