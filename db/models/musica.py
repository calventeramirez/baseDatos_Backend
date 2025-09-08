from pydantic import  BaseModel

class Musica(BaseModel):
    id: str | None
    titulo: str
    artista: str
    tipoArtista: str
    tipoMusica: str
    tipoMusicaClasica: str | None
    idioma: str
    discografica: str
    anoGrab:int
    formato: str
    colecciones: str
    album: str
    numPista: int
    conciertos: str
    fotoPortada: str | None
    fotoContraportada: str | None
    memo: str | None
    resenaBio: str | None
