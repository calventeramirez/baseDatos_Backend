def musicas_schema(musica) -> dict:
    return {
        "id": str(musica["_id"]),
        "titulo": str(musica["titulo"]),
        "artista": str(musica["artista"]),
        "tipoArtista": str(musica["tipoArtista"]),
        "tipoMusica": str(musica["tipoMusica"]),
        "tipoMusicaClasica": str(musica["tipoMusicaClasica"]) if musica["tipoMusicaClasica"] is not None else "",
        "idioma": str(musica["idioma"]),
        "discografica": str(musica["discografica"]),
        "anoGrab": int(musica["anoGrab"]),
        "formato": str(musica["formato"]),
        "colecciones": str(musica["colecciones"]),
        "album": str(musica["album"]),
        "numPista": int(musica["numPista"]),
        "conciertos": str(musica["conciertos"]),
        "fotoPortada": str(musica["fotoPortada"]) if musica["fotoPortada"] is not None else "",
        "fotoContraportada": str(musica["fotoContraportada"]) if musica["fotoContraportada"] is not None else "",
        "memo": str(musica["memo"]) if musica["memo"] is not None else "",
        "resenaBio": str(musica["resenaBio"]) if musica["resenaBio"] is not None else "",
    }

def musicas_schema_list(musicas) -> list:
    return [musicas_schema(musica) for musica in musicas]