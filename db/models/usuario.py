from pydantic import BaseModel #Para crear clases con las que trabajar

class Usuario(BaseModel):
    id: str | None
    username: str
    password: str