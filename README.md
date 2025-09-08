# 🚀 Backend - Biblioteca Digital

API REST desarrollada con Python, FastAPI y MongoDB para la gestión integral de una biblioteca digital que incluye múltiples tipos de contenido cultural y educativo.

## 🏗️ Arquitectura

- **Framework**: FastAPI (Python 3.8+)
- **Base de Datos**: MongoDB
- **ODM**: Motor (MongoDB Async Driver)
- **Validación**: Pydantic
- **Documentación**: OpenAPI/Swagger automática
- **CORS**: Habilitado para desarrollo frontend

## 📚 Colecciones Gestionadas

El sistema maneja 6 tipos principales de contenido:

- **📖 Libros** - Literatura y publicaciones
- **🎵 Música** - Discos y álbumes (incluye música clásica especializada)
- **🎬 Videoteca** - Contenido audiovisual
- **💿 CD-Rom** - Software y multimedia interactiva
- **📰 Revistas** - Publicaciones periódicas
- **🎨 Arte** - Cuadros y esculturas

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- MongoDB 4.4 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio**
```bash
  git clone https://github.com/calventeramirez/baseDatos_Backend.git
  cd baseDatos_Backend
```

2. **Crear entorno virtual**
```bash
  python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
  pip install -r requirements.txt
```

5. **Ejecutar el servidor**
```bash
  fastapi dev main.py
```

6. **Acceder a la documentación**
```
http://localhost:8000/docs
```

## 📋 API Endpoints

### 📖 Libros
```
GET    /libros/             # Lista todos los libros
GET    /libros/{id}         # Obtiene un libro específico
POST   /libros/             # Crear nuevo libro
PUT    /libros/             # Actualizar libro
DELETE /libros/{id}         # Eliminar libro
```

### 🎵 Música
```
GET    /musica/              # Lista toda la música
GET    /musica/{id}          # Obtiene un disco específico
POST   /musica/              # Crear nuevo disco
PUT    /musica/              # Actualizar disco
DELETE /musica/{id}          # Eliminar disco
```

### 🎬 Videoteca
```
GET    /videoteca/           # Lista videos
GET    /videoteca/{id}       # Obtiene video específico
POST   /videoteca/           # Crear nuevo video
PUT    /videoteca/           # Actualizar video
DELETE /videoteca/{id}       # Eliminar video
```

### 💿 CD-Rom
```
GET    /cdrom/               # Lista CD-Roms
GET    /cdrom/{id}           # Obtiene CD-Rom específico
POST   /cdrom/               # Crear nuevo CD-Rom
PUT    /cdrom/               # Actualizar CD-Rom
DELETE /cdrom/{id}           # Eliminar CD-Rom
```

### 📰 Revistas
```
GET    /revistas/            # Lista revistas
GET    /revistas/{id}        # Obtiene revista específica
POST   /revistas             # Crear nueva revista
PUT    /revistas/            # Actualizar revista
DELETE /revistas/{id}        # Eliminar revista
```

### 🎨 Arte
```
GET    /arte/                # Lista obras de arte
GET    /arte/{id}            # Obtiene obra específica
POST   /arte/                # Crear nueva obra
PUT    /arte/                # Actualizar obra
DELETE /arte/{id}            # Eliminar obra
```

## 📊 Modelos de Datos

### Libros
```python
class Libros(BaseModel):
    id: str | None
    titulo: str
    autor: str
    categoria: str
    subcategoria: str | None
    enciclopedia: str | None
    colecciones: str | None
    editorial: str
    idioma: str
    numPag: int
    yearPub: int
    isbn: str
    depositoLegal: str
    fotoPortada: str | None
    fotoContraportada: str | None
```

### Música
```python
class Musica(BaseModel):
    id: str | None
    titulo: str
    artista: str
    tipoArtista: str
    tipoMusica: str
    tipoMusicaClasica: str | None
    idioma: str
    discografica: str
    anoGrab:int
    formato: str
    colecciones: str
    album: str
    numPista: int
    conciertos: str
    fotoPortada: str | None
    fotoContraportada: str | None
    memo: str | None
    resenaBio: str | None
```

### Videos
```python
class Videos(BaseModel):
    id: str | None
    tituloEsp: str
    tituloOrg: str | None
    tematica: str
    director: str
    protagonistas: str
    companiaCinematografica: str
    duracion: int
    idiomasAudios: str
    idiomasSubtitulos: str
    formato: str
    pais: str
    nacionalidad: str
    portada: str | None
    argumento: str
```

### CD-ROM
```python
class CDROM(BaseModel):
    id: str | None
    titulo: str
    tematica: str
    duracion: float | None
    yearGrab: int
    coleccion: str | None
```

### Revistas
```python
class Revista(BaseModel):
    id: str | None
    titulo: str
    tematica: str
    editorial: str
    fechaEdicion: int | None
    numPag: int | None
    numRevista: int | None
    fotoPortada: str | None
```

### Cuadros y Esculturas
```python
class Arte(BaseModel):
    id: str | None
    titulo: str
    autor: str
    tematica: str
    tecnicaPictorica: str | None
    tecnicaEscultorica: str | None
    certificado: bool
    altura: str | None
    anchura: str | None
    peso: str | None
```


## 📁 Estructura del Proyecto

```
baseDatos_Backend/
├── db/
|   ├── models/              # Modelos Pydantic
│   │   ├── arte.py
│   │   ├── cdrom.py
│   │   ├── libros.py
│   │   ├── musica.py
│   │   ├── revista.py
│   │   ├── usuario.py
│   │   └── videos.py
|   ├── schema/              # Modelos Pydantic
│   │   ├── arte.py
│   │   ├── cdrom.py
│   │   ├── libros.py
│   │   ├── musica.py
│   │   ├── revista.py
│   │   ├── usuario.py
│   │   └── videos.py
|   └── client.py
├── routers/
│   ├── arte.py
│   ├── cdrom.py
│   ├── libros.py
│   ├──  musica.py
│   ├── revista.py
│   ├──  usuario.py
│   └── videos.py
├── main.py                  # Aplicación principal FastAPI
├── requirements.txt         # Dependencias Python
└── README.md
```

## 🔧 Configuración de MongoDB

### Colecciones de Base de Datos
- `libros` - Almacena información de libros
- `musica` - Catálogo musical
- `videoteca` - Archivo de videos
- `cdrom` - Colección de CD-Roms
- `revistas` - Hemeroteca
- `arte` - Galería de arte


## 🎵 Características Especiales - Música Clásica

El sistema incluye manejo especializado para música clásica con los siguientes períodos:

- **Medieval o Antigua**
- **Renacentista**  
- **Clasicista o Neoclásica**
- **Romántica**
- **Nacionalista**
- **Contemporánea Politonista**
- **Contemporánea Dodecafónica**
- **Contemporánea Atonalista**

Cada período puede tener subclasificaciones como: Óperas, Sinfonías, Música de cámara, Oratorios, Misas, Sonatas, Poemas Sinfónicos, Compositores.

## 🚀 Características de FastAPI

### Documentación Automática
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Validación Automática
- Validación de tipos con Pydantic
- Serialización automática JSON
- Manejo de errores HTTP estandarizado
- Documentación de schemas automática

### Performance
- Programación asíncrona nativa
- Validación de datos ultra-rápida
- Compatible con Python type hints
- Soporte para operaciones concurrentes

## 🔒 Seguridad y CORS

### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Próximas Implementaciones de Seguridad
- [ ] JWT Authentication
- [ ] Rate Limiting
- [ ] API Key Authentication
- [ ] OAuth2 Integration

## 📦 Dependencias Principales

```txt
fastapi>=0.104.0
motor>=3.3.0
pydantic>=2.4.0
python-multipart>=0.0.6
python-dotenv>=1.0.0
```

### Logs
- Configuración con Python logging
- Rotación automática de logs
- Niveles configurables por entorno

## 🤝 Contribución

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Estándares de Código
- **PEP 8** para estilo de código Python
- **Type hints** obligatorios
- **Docstrings** en funciones públicas
- **Tests** para nuevas funcionalidades

## 📞 Soporte

Para reportar bugs o solicitar features:
- **Issues**: [GitHub Issues](https://github.com/calventeramirez/baseDatos_Backend/issues)
- **Email**: calventeramirez@outlook.com

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

**🔧 Backend API - Biblioteca Digital** | *Potenciando la gestión cultural con tecnología moderna*