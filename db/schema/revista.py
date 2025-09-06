def revistas_schema(revista) -> dict:
    return {
        "id": str(revista["_id"]),
        "titulo": str(revista["titulo"]),
        "tematica": str(revista["tematica"]),
        "editorial": str(revista["editorial"]),
        "fechaEdicion": int(revista["fechaEdicion"]) if revista["fechaEdicion"] is not None else "",
        "numPag": int(revista["numPag"]) if revista["numPag"] is not None else "",
        "numRevista": int(revista["numRevista"]) if revista["numRevista"] is not None else "",
        "fotoPortada": str(revista["fotoPortada"]) if revista["fotoPortada"] is not None else "",

    }

def revistas_schema_list(revistas) -> list:
    return [revistas_schema(revista) for revista in revistas]