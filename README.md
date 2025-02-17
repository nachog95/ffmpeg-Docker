
# Microservicio FastAPI con FFmpeg para n8n

¡Bienvenido a nuestro microservicio de compresión/conversión de audio!  
Este proyecto usa **FastAPI** y **FFmpeg** para procesar archivos de audio (por ejemplo, comprimirlos a distintos bitrates) y devolverlos vía API.

## Tabla de Contenidos
- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Ejecución](#instalación-y-ejecución)
  - [Docker Compose](#docker-compose)
- [Uso](#uso)
  - [Endpoint de Salud](#endpoint-de-salud)
  - [Endpoint de Compresión](#endpoint-de-compresión)
- [Ejemplo de Integración con n8n](#ejemplo-de-integración-con-n8n)
  - [Ejemplo de automatización (Podcast_to_Telegram.json)](#ejemplo-de-automatización-podcast_to_telegramjson)
- [Personalización de Parámetros FFmpeg](#personalización-de-parámetros-ffmpeg)
- [Notas y Consejos](#notas-y-consejos)
- [Licencia](#licencia)

---

## Descripción
Este microservicio expone un **endpoint** para recibir un archivo de audio en formato multipart/form-data, procesarlo usando **FFmpeg** (por ejemplo, bajando el bitrate o cambiando la frecuencia de muestreo) y devolverlo ya convertido/comprimido.

**Tecnologías principales**:
- [FastAPI](https://fastapi.tiangolo.com/)
- [FFmpeg](https://ffmpeg.org/)
- [Docker & Docker Compose](https://www.docker.com/)

---

## Requisitos
- **Docker** y **Docker Compose** instalados en tu sistema.
- (Opcional) [Python 3.9+](https://www.python.org/downloads/) si quieres probarlo localmente sin Docker.

---

## Estructura del Proyecto

```
.
├── fastapi-ffmpeg-compress    # Carpeta con el microservicio
│   ├── main.py                # Código principal de la API (FastAPI + FFmpeg)
│   ├── Dockerfile             # Imagen Docker (Python + FFmpeg)
│   ├── docker-compose.yml     # Orquestación con Docker Compose
│   └── requirements.txt       # Dependencias de Python (fastapi, uvicorn, etc.)
├── Podcast_to_Telegram (2).json   # Ejemplo de flujo/automatización en n8n
└── README.md                  # Este fichero
```

---

## Instalación y Ejecución

### Docker Compose
1. Clona este repositorio:

   ```bash
   git clone https://github.com/nachog95/ffmpeg-Docker.git
   ```
    ```bash
   cd ffmpeg-Docker
    ```
    ```bash
   cd astapi-ffmpeg-compress
   ```

2. Construye la imagen y levanta el contenedor:

   ```bash
   docker compose build
   ```
   ```bash
   docker compose up
   ```
   Esto:
   - Construirá la imagen basada en el `Dockerfile`.
   - Ejecutará tu servicio en el puerto **8000** por defecto.

3. Verifica que todo esté en marcha visitando en tu navegador:
   ```
   http://localhost:8000/health
   ```
   Si el servicio está bien, verás:
   ```json
   { "status": "OK" }
   ```

---

## Uso
Una vez que el servicio está en marcha, la API estará disponible en `http://localhost:8000` (o en tu IP pública si lo has desplegado en un servidor).

### Endpoint de Salud
- **GET** `/health`

  **Respuesta**:
  ```json
  { "status": "OK" }
  ```

### Endpoint de Compresión
- **POST** `/compress_audio`
  - **Body (multipart/form-data)**:
    - Campo **file**: archivo de audio que deseas enviar para comprimir.
  - **Retorno**: un archivo de audio comprimido, en formato MP3 (o el que hayas configurado).

**Ejemplo con `curl`:**
```bash
curl -X POST "http://localhost:8000/compress_audio" \
  -F "file=@/ruta/a/tu_audio.m4a" \
  --output "resultado.mp3"
```
Esto enviará `tu_audio.m4a` y descargará la respuesta comprimida como `resultado.mp3`.

---

## Ejemplo de Integración con n8n
Puedes integrar este microservicio con [n8n](https://n8n.io/) de muchas maneras. Lo básico es:

1. Usar un **nodo HTTP Request** (método POST).
2. URL: `http://localhost:8000/compress_audio` (o `host.docker.internal:8000` si n8n está en otro contenedor en Docker Desktop).
3. Body Content Type: `Form-Data`.
4. Añade un campo:
   - **Name**: `file`
   - **Value**: la propiedad binaria que contenga el audio.
5. Ejecuta el nodo; obtendrás de vuelta un archivo binario comprimido.

### Ejemplo de automatización (`Podcast_to_Telegram.json`)
En la carpeta raíz se incluye un fichero JSON: **`Podcast_to_Telegram (2).json`**, que representa un flujo de n8n que:

1. **Lee un feed RSS** (mediante un nodo *RSS Feed Trigger*), para obtener los últimos episodios de un podcast.  
2. **Genera o define el Caption** del mensaje con un nodo *OpenAI*, usando el contenido del RSS como prompt.  
3. **Descarga el audio** (nodo *HTTP Request*).  
4. **Llama a este microservicio** (otro *HTTP Request*) para comprimir el audio.  
5. **Renombra el binario** con el título del episodio (nodo *Code*).  
6. **Envía el audio y la descripción a Telegram** (nodo *Telegram*).  

Puedes importar el flujo **`Podcast_to_Telegram (2).json`** directamente en n8n para probar todo el pipeline de forma automatizada.

---

## Personalización de Parámetros FFmpeg
En `main.py`, verás la parte del código donde se define el comando `ffmpeg`. Por ejemplo:
```python
command = [
    "ffmpeg",
    "-y",           # Sobrescribir archivo sin preguntar
    "-i", input_filename,
    "-b:a", "128k", # Ajusta el bitrate
    output_filename
]
```
Puedes modificar flags como:
- `-ar 22050` (frecuencia de muestreo)
- `-ac 1` (convertir a mono)
- `-b:a 64k` (bitrate)
- O incluso usar otro códec: `-c:a libopus`.

---

## Notas y Consejos
1. **Persistencia de Archivos**  
   Actualmente, el servicio maneja los archivos temporalmente dentro del contenedor y los borra tras la conversión. Si quieres guardar el resultado en un bucket (S3, etc.), tendrás que ajustar el código.

2. **Seguridad y Validaciones**  
   ffmpeg es potente, pero conviene validar el formato/tamaño de los archivos, especialmente en entornos de producción.

3. **Escalabilidad**  
   Para procesar varios archivos simultáneamente, se puede escalar contenedores en Kubernetes o usar una cola (ej. RabbitMQ, Redis) para colas de trabajo.


