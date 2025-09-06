from fastapi import FastAPI, APIRouter, status, HTTPException
from db.models.videos import Videos
from db.schema.videos import videos_schema, videos_schema_list
from db.client import db_client
from bson.objectid import ObjectId

router = APIRouter(prefix="/videos", tags=["Videos"], responses={status.HTTP_404_NOT_FOUND: {"Mensaje": "No encontrado el video"}})

@router.get("/", response_model=list[Videos])
async def get_all_videos():
    return videos_schema_list(db_client.videos.find())

@router.get("/{id}", response_model=Videos)
async def get_video(id: str):
    #Valido ID
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Invalida")

    video = db_client.videos.find_one({"_id": ObjectId(id)})

    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El video no existe")

    return Videos(**videos_schema(video))

@router.post("/", response_model=Videos, status_code=status.HTTP_201_CREATED)
async def create_video(video: Videos):
    if search_videos("tituloEsp", video.tituloEsp) is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="La película ya existe")

    video_dict = dict(video)
    del video_dict["id"] #Se borra para que autogenere en mongo

    id = db_client.videos.insert_one(video_dict).inserted_id
    new_video = videos_schema(db_client.videos.find_one({"_id": ObjectId(id)}))
    return Videos(**new_video)

@router.put("/", response_model=Videos)
async def update_video(video: Videos):
    video_dict = dict(video)
    del video_dict["id"]

    updated_video = db_client.videos.find_one_and_update({"tituloEsp": video.tituloEsp},
                                                         {"$set": video_dict},
                                                         return_document=True)
    if not updated_video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video no encontrado")

    return Videos(**videos_schema(updated_video))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(id: str):
    found = db_client.videos.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "No se ha encontrado el video para eliminarlo"}


def search_videos(field:str, key):
    video = db_client.videos.find_one({field: key})
    if video:
        return videos_schema(video)
    return None