from pydantic import  BaseModel

class Arte(BaseModel):
    id: str | None
    titulo: str
    autor: str
    tematica: str
    tecnicaPictorica: str | None
    tecnicaEscultorica: str | None
    certificado: bool
    altura: str | None
    anchura: str | None
    peso: str | None