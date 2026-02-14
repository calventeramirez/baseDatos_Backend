from db.client import db_client


def create_indexes():
    """Crear índices para optimizar búsquedas"""

    # Índice para búsqueda por título (case-insensitive)
    db_client.libros.create_index([("titulo", 1)])

    # Índice para búsqueda por autor
    db_client.libros.create_index([("autor", 1)])

    # Índice para ISBN (único)
    db_client.libros.create_index([("isbn", 1)], unique=True)

    # Índice de texto completo para búsquedas más avanzadas (opcional)
    db_client.libros.create_index([
        ("titulo", "text"),
        ("autor", "text")
    ])

    print("✅ Índices creados correctamente")


if __name__ == "__main__":
    create_indexes()