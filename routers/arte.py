from fastapi import FastAPI, APIRouter, status, HTTPException
from db.models.arte import Arte
from db.schema.arte import artes_schema, artes_schema_list
from db.client import db_client
from bson.objectid import ObjectId

router = APIRouter(prefix="/arte", tags=["Arte"], responses={status.HTTP_404_NOT_FOUND: {"Mensaje": "No encontrado el video"}})

@router.get("/", response_model=list[Arte])
async def get_all_arte():
    return artes_schema_list(db_client.arte.find())

@router.get("/{id}", response_model=Arte)
async def get_arte(id: str):
    #Valido ID
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Invalida")

    arte = db_client.arte.find_one({"_id": ObjectId(id)})

    if not arte:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cuadro o escultura no existe")

    return Arte(**artes_schema(arte))

@router.post("/", response_model=Arte, status_code=status.HTTP_201_CREATED)
async def create_arte(arte: Arte):
    if search_arte("titulo", arte.titulo) is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="El cuadro o escultura ya existe")

    arte_dict = dict(arte)
    del arte_dict["id"] #Se borra para que autogenere en mongo

    id = db_client.arte.insert_one(arte_dict).inserted_id
    new_arte = artes_schema(db_client.arte.find_one({"_id": ObjectId(id)}))
    return Arte(**new_arte)

@router.put("/", response_model=Arte)
async def update_arte(arte: Arte):
    arte_dict = dict(arte)
    print(arte_dict)
    del arte_dict["id"]
    print(arte_dict)
    updated_arte = db_client.arte.find_one_and_update({"_id": ObjectId(arte.id)},
                                                         {"$set": arte_dict},
                                                         return_document=True)
    print(updated_arte)
    if not updated_arte:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuadro o Escultura no encontrado")

    return Arte(**artes_schema(updated_arte))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(id: str):
    found = db_client.arte.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "No se ha encontrado el cuadro o la escultura para eliminarlo"}

def search_arte(field:str, key):
    arte = db_client.arte.find_one({field: key})
    if arte:
        return artes_schema(arte)
    return None