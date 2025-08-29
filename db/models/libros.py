from pydantic import  BaseModel

class Libros(BaseModel):
    id: str | None
    titulo: str
    autor: str
    categoria: str
    subcategoria: str | None
    enciclopedia: str | None
    colecciones: str | None
    editorial: str
    idioma: str
    numPag: int
    yearPub: int
    isbn: str
    depositoLegal: str
    fotoPortada: str | None
    fotoContraportada: str | None