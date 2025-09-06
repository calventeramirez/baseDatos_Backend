def artes_schema(arte) -> dict:
    return {
        "id": str(arte["_id"]),
        "titulo": str(arte["titulo"]),
        "autor": str(arte["autor"]),
        "tematica": str(arte["tematica"]),
        "tecnicaPictorica": str(arte["tecnicaPictorica"]) if arte["tecnicaPictorica"] is not None else "",
        "tecnicaEscultorica": str(arte["tecnicaEscultorica"]) if arte["tecnicaEscultorica"] is not None else "",
        "certificado": bool(arte["certificado"]),
        "altura": float(arte["altura"]) if arte["altura"] is not None else "",
        "anchura": float(arte["anchura"]) if arte["anchura"] is not None else "",
        "peso": float(arte["peso"]) if arte["peso"] is not None else "",
    }

def artes_schema_list(artes) -> list:
    return [artes_schema(arte) for arte in artes]