from fastapi import FastAPI, APIRouter, status, HTTPException, Query
from db.models.libros import Libros
from db.client import db_client
from db.schema.libros import libros_schema, libros_schema_list
from bson.objectid import ObjectId
from typing import Optional
import math

router = APIRouter(
    prefix="/libros",
    tags=["Libros"],
    responses={status.HTTP_404_NOT_FOUND: {"Mensaje": "No encontrado el libro"}}
)


# 👇 NUEVO ENDPOINT CON PAGINACIÓN
@router.get("/")
async def get_all_libros(
        page: int = Query(1, ge=1, description="Número de página"),
        limit: int = Query(10, ge=1, le=100, description="Libros por página"),
        search: Optional[str] = Query(None, description="Buscar por título o autor")
):
    # Calcular skip
    skip = (page - 1) * limit

    # Construir filtro de búsqueda
    filter_query = {}
    if search and search.strip():
        filter_query = {
            "$or": [
                {"titulo": {"$regex": search, "$options": "i"}},
                {"autor": {"$regex": search, "$options": "i"}}
            ]
        }

    # Obtener total de documentos
    total = db_client.libros.count_documents(filter_query)

    # Obtener libros paginados y ordenados por _id descendente (más nuevos primero)
    libros_cursor = db_client.libros.find(filter_query).sort("_id", -1).skip(skip).limit(limit)
    libros = libros_schema_list(libros_cursor)

    # Calcular total de páginas
    total_pages = math.ceil(total / limit) if total > 0 else 0

    # 👇 DEVOLVER EN EL FORMATO ESPERADO
    return {
        "results": libros,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    }


@router.get("/{id}", response_model=Libros)
async def get_libro(id: str):
    # Valido id
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID invalida"
        )

    libro = db_client.libros.find_one({"_id": ObjectId(id)})

    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="libro no encontrado"
        )

    return Libros(**libros_schema(libro))


@router.post("/", response_model=Libros, status_code=status.HTTP_201_CREATED)
async def create_libro(libro: Libros):
    if search_libros("isbn", libro.isbn) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El libro ya existe"
        )

    libro_dict = dict(libro)
    del libro_dict["id"]

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
        return_document=True
    )

    if not update_libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha encontrado el libro"
        )

    return Libros(**libros_schema(update_libro))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_libro(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID inválida"
        )

    found = db_client.libros.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha encontrado el libro para eliminarlo"
        )

    return None


def search_libros(field: str, key):
    libro = db_client.libros.find_one({field: key})
    if libro:
        return libros_schema(libro)
    return None