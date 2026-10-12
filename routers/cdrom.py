from fastapi import FastAPI, APIRouter, status, HTTPException, Query
from db.client import db_client
from db.models.cdrom import CDROM
from db.schema.cdrom import cdroms_schema, cdroms_schema_list
from bson.objectid import ObjectId
from typing import Optional
import math
import re

router = APIRouter(prefix="/cdrom", tags=["CD-ROM"], responses={status.HTTP_404_NOT_FOUND: {"Mensaje": "No encontrado el CD-ROM"}})

#@router.get("/", response_model=list[CDROM])
#async def get_all_cdrom():
#    return cdroms_schema_list(db_client.cdroms.find())

SEARCH_FIELDS = ["titulo", "tematica", "coleccion"]

@router.get("/")
async def get_all_cdrom(
        page: int = Query(1, ge=1, description="Número de página"),
        limit: int = Query(10, ge=1, le=100, description="CD-ROM por página"),
        search: Optional[str] = Query(None, description="Buscar por título, temática o colección")
):
    skip = (page - 1) * limit

    filter_query = {}
    if search and search.strip():
        regex = {"$regex": re.escape(search.strip()), "$options": "i"}
        filter_query = {"$or": [{field: regex} for field in SEARCH_FIELDS]}

    total = db_client.cdroms.count_documents(filter_query)

    cdroms_cursor = db_client.cdroms.find(filter_query).sort("_id", -1).skip(skip).limit(limit)
    cdroms = cdroms_schema_list(cdroms_cursor)

    total_pages = math.ceil(total / limit) if total > 0 else 0

    return {
        "results": cdroms,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    }

@router.get("/{id}", response_model=CDROM)
async def get_cdrom(id: str):
    # Valido id
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID invalida")
    libro = db_client.cdroms.find_one({"_id": ObjectId(id)})

    if not libro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="CDROM no encontrado")

    return CDROM(**cdroms_schema(libro))

@router.post("/", response_model=CDROM, status_code=status.HTTP_201_CREATED)
async def create_cdrom(cdrom: CDROM):
    if search_cdroms("titulo", cdrom.titulo) is not None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "El libro ya existe")

    cdrom_dict = dict(cdrom)
    del cdrom_dict["id"] #Se borra para que autogenere en mongo

    id = db_client.cdroms.insert_one(cdrom_dict).inserted_id

    new_cdrom = cdroms_schema(db_client.cdroms.find_one({"_id": id}))

    return CDROM(**new_cdrom)

@router.put("/", response_model=CDROM)
async def update_cdrom(cdrom: CDROM):
    cdrom_dict = dict(cdrom)
    del cdrom_dict["id"]
    update_cdrom = db_client.cdroms.find_one_and_update(
        {"_id": ObjectId(cdrom.id)},
        {"$set": cdrom_dict},
        return_document=True)
    if not update_cdrom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No se ha encontrado el cdrom")

    return CDROM(**cdroms_schema(update_cdrom))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cdrom(id: str):
    found = db_client.cdroms.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha encontrado el cdrom para eliminarlo"}

def search_cdroms(field:str, key):
    cdrom = db_client.cdroms.find_one({field: key})
    if cdrom:
        return cdroms_schema(cdrom)
    return None