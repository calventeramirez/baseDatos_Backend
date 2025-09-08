from fastapi import FastAPI, APIRouter, status, HTTPException
from db.models.musica import Musica
from db.schema.musica import musicas_schema, musicas_schema_list
from db.client import db_client
from bson.objectid import ObjectId

router = APIRouter(prefix="/musica", tags=["Musica"], responses={status.HTTP_404_NOT_FOUND: {"Mensaje": "No encontrado la musica"}})

@router.get("/", response_model=list[Musica])
async def get_all_musicas():
    return musicas_schema_list(db_client.musicas.find())

@router.get("/{id}", response_model=Musica)
async def get_musica(id: str):
    #Valido ID
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Invalida")

    musica = db_client.musicas.find_one({"_id": ObjectId(id)})

    if not musica:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El disco de musica no existe")

    return Musica(**musicas_schema(musica))

@router.post("/", response_model=Musica, status_code=status.HTTP_201_CREATED)
async def create_musica(musica: Musica):
    if search_musica("titulo", musica.titulo) is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="El disco de musica ya existe")

    musica_dict = dict(musica)
    del musica_dict["id"] #Se borra para que autogenere en mongo

    id = db_client.musicas.insert_one(musica_dict).inserted_id
    new_musica = musicas_schema(db_client.musicas.find_one({"_id": ObjectId(id)}))
    return Musica(**new_musica)

@router.put("/", response_model=Musica)
async def update_arte(musica: Musica):
    musica_dict = dict(musica)
    print(musica_dict)
    del musica_dict["id"]
    print(musica_dict)
    updated_musica = db_client.musicas.find_one_and_update({"_id": ObjectId(musica.id)},
                                                         {"$set": musica_dict},
                                                         return_document=True)
    print(updated_musica)
    if not updated_musica:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El disco de musica no encontrado")

    return Musica(**musicas_schema(updated_musica))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(id: str):
    found = db_client.musicas.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "No se ha encontrado el disco de musica para eliminarlo"}

def search_musica(field:str, key):
    musica = db_client.musicas.find_one({field: key})
    if musica:
        return musicas_schema(musica)
    return None