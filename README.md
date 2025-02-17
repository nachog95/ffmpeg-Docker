# ffmpeg-Docker
# FastAPI FFmpeg Compress

Este proyecto es una API desarrollada con FastAPI que utiliza FFmpeg para comprimir archivos de video.
Se proporciona soporte para Docker para facilitar su despliegue.

## Requisitos

- Python 3.8+
- FFmpeg instalado
- FastAPI y otras dependencias (especificadas en `requirements.txt`)
- Docker (opcional, para ejecución en contenedor)

## Instalación

### Instalación manual

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd fastapi-ffmpeg-compress
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar la API:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Instalación con Docker

1. Construir la imagen Docker:
   ```bash
   docker build -t fastapi-ffmpeg .
   ```

2. Ejecutar el contenedor:
   ```bash
   docker run -p 8000:8000 fastapi-ffmpeg
   ```

O bien, usando `docker-compose`:
   ```bash
   docker-compose up -d
   ```

## Uso

Una vez la API esté en ejecución, se puede acceder a la documentación interactiva de FastAPI en:

```
http://localhost:8000/docs
```

Desde ahí se pueden probar los endpoints de la API.

## Autor

Desarrollado por [Tu Nombre].

