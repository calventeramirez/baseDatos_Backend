def libros_schema(libro) -> dict:
    return {
        "id": str(libro["_id"]),
        "titulo": str(libro["titulo"]),
        "autor": str(libro["autor"]),
        "categoria": str(libro["categoria"]),
        "subcategoria": str(libro["subcategoria"]) if libro["subcategoria"] is not None else "",
        "enciclopedia": str(libro["enciclopedia"]) if libro["enciclopedia"] is not None else "",
        "colecciones": str(libro["colecciones"]) if libro["colecciones"] is not None else "",
        "editorial": str(libro["editorial"]),
        "idioma": str(libro["idioma"]),
        "numPag": int(libro["numPag"]),
        "yearPub": int(libro["yearPub"]),
        "isbn": str(libro["isbn"]),
        "depositoLegal": str(libro["depositoLegal"]),
        "fotoPortada": str(libro["fotoPortada"]) if libro["fotoPortada"] is not None else "",
        "fotoContraportada": str(libro["fotoContraportada"]) if libro["fotoContraportada"] is not None else "",
    }

def libros_schema_list(libros) -> list:
    return [libros_schema(libro) for libro in libros]