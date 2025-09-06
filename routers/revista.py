from fastapi import FastAPI, APIRouter, status, HTTPException
from db.models.revista import Revista
from db.schema.revista import revistas_schema, revistas_schema_list
from db.client import db_client
from bson.objectid import ObjectId

router = APIRouter(prefix="/revista", tags=["Revistas"], responses={status.HTTP_404_NOT_FOUND: {"Mensaje": "No encontrado la revista"}})

@router.get("/", response_model=list[Revista])
async def get_all_revistas():
    return revistas_schema_list(db_client.revistas.find())

@router.get("/{id}", response_model=Revista)
async def get_revista(id: str):
    #Valido ID
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Invalida")

    revista = db_client.revistas.find_one({"_id": ObjectId(id)})

    if not revista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La revista no existe")

    return Revista(**revistas_schema(revista))

@router.post("/", response_model=Revista, status_code=status.HTTP_201_CREATED)
async def create_revista(revista: Revista):
    if search_revistas("titulo", revista.titulo) is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="La revista ya existe")

    revista_dict = dict(revista)
    del revista_dict["id"] #Se borra para que autogenere en mongo

    id = db_client.revistas.insert_one(revista_dict).inserted_id
    new_revista = revistas_schema(db_client.revistas.find_one({"_id": ObjectId(id)}))
    return Revista(**new_revista)

@router.put("/", response_model=Revista)
async def update_revista(revista: Revista):
    revista_dict = dict(revista)
    print(revista_dict)
    del revista_dict["id"]
    print(revista_dict)
    updated_revista = db_client.revistas.find_one_and_update({"_id": ObjectId(revista.id)},
                                                         {"$set": revista_dict},
                                                         return_document=True)
    print(updated_revista)
    if not updated_revista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La revista no encontrado")

    return Revista(**revistas_schema(updated_revista))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_revista(id: str):
    found = db_client.revistas.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "No se ha encontrado la revista para eliminarla"}

def search_revistas(field:str, key):
    revista = db_client.revistas.find_one({field: key})
    if revista:
        return revistas_schema(revista)
    return None