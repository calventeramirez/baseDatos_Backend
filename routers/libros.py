from fastapi import FastAPI, APIRouter, status, HTTPException
from db.models.libros import Libros
from db.client import db_client
from db.schema.libros import libros_schema, libros_schema_list
from bson.objectid import  ObjectId

router = APIRouter(prefix="/libros", tags=["libros"], responses={status.HTTP_404_NOT_FOUND: {"Mensaje": "No encontrado el libro"}})

@router.get("/", response_model=list[Libros])
async def get_all_libros():
    return libros_schema_list(db_client.libros.find())

@router.get("/{id}", response_model=Libros)
async def get_libro(id: str):
    #Valido id
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID invalida")
    libro = db_client.libros.find_one({"_id": ObjectId(id)})

    if not libro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="libro no encontrado")

    return Libros (**libros_schema(libro))

@router.post("/", response_model=Libros, status_code=status.HTTP_201_CREATED)
async def create_libro(libro: Libros):
    if search_libros("isbn", libro.isbn) is not None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "El libro ya existe")

    libro_dict = dict(libro)
    del libro_dict["id"] #Se borra para que autogenere en mongo

    id = db_client.libros.insert_one(libro_dict).inserted_id

    new_libro = libros_schema(db_client.libros.find_one({"_id": id}))

    return Libros(**new_libro)

@router.put("/", response_model=Libros)
async def update_libro(libro: Libros):
    libro_dict = dict(libro)
    del libro_dict["id"]
    update_libro = db_client.libros.find_one_and_update(
        {"_id": ObjectId(libro.id)},
        {"$set": libro_dict},
        return_document= True )
    if not update_libro:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail="No se ha encontrado el libro")

    return Libros(**libros_schema(update_libro))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_libro(id: str):
    found = db_client.libros.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha encontrado el libro para eliminarlo"}


def search_libros(field:str, key):
    libro = db_client.libros.find_one({field: key})
    if libro:
        return libros_schema(libro)
    return None