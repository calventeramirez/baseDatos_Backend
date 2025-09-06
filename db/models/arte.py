from pydantic import  BaseModel

class Arte(BaseModel):
    id: str | None
    titulo: str
    autor: str
    tematica: str
    tecnicaPictorica: str | None
    tecnicaEscultorica: str | None
    certificado: bool
    altura: float | None
    anchura: float | None
    peso: float | None