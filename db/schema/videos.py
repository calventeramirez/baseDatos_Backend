def videos_schema(video) -> dict:
    return {
        "id": str(video["_id"]),
        "tituloEsp": str(video["tituloEsp"]),
        "tituloOrg": str(video["tituloOrg"]) if video["tituloOrg"] is not None else "",
        "tematica": str(video["tematica"]),
        "director": str(video["director"]),
        "protagonistas": str(video["protagonistas"]),
        "companiaCinematografica": str(video["companiaCinematografica"]),
        "duracion": str(video["duracion"]),
        "idiomasAudios": str(video["idiomasAudios"]),
        "idiomasSubtitulos": str(video["idiomasSubtitulos"]),
        "formato": str(video["formato"]),
        "pais": str(video["pais"]),
        "nacionalidad": str(video["nacionalidad"]),
        "portada": str(video["portada"]) if video["portada"] is not None else "",
        "argumento": str(video["argumento"]),
    }

def videos_schema_list(videos) -> list:
    return [videos_schema(video) for video in videos]