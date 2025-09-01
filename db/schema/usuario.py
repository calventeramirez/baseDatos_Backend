def usuario_schema(usuario) -> dict:
    return {
        "id": str(usuario["id"]),
        "username": usuario["username"],
        "password": usuario["password"],
    }