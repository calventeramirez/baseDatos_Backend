def cdroms_schema(cdrom) -> dict:
    return {
        "id": str(cdrom["_id"]),
        "titulo": str(cdrom["titulo"]),
        "tematica": str(cdrom["tematica"]),
        "duracion": str(cdrom["duracion"]) if cdrom["duracion"] is not None else "",
        "yearGrab": str(cdrom["yearGrab"]) if cdrom["yearGrab"] is not None else "",
        "coleccion": str(cdrom["coleccion"]) if cdrom["coleccion"] is not None else "",
    }

def cdroms_schema_list(cdroms) -> list:
    return [cdroms_schema(cdrom) for cdrom in cdroms]