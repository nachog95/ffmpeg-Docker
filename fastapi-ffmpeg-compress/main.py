# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import subprocess
import uuid
import os
import io

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.post("/compress_audio")
async def compress_audio(file: UploadFile = File(...)):
    # 1. Generamos nombres de archivo temporales únicos
    input_filename = f"{uuid.uuid4()}_{file.filename}"
    output_filename = f"{uuid.uuid4()}.mp3"

    # 2. Guardamos el archivo subido en disco
    with open(input_filename, "wb") as f:
        f.write(await file.read())

    # 3. Comprimir con ffmpeg
    #    -b:a 128k = bitrate de 128 Kbps (puedes cambiarlo)
    command = [
    "ffmpeg",
    "-y",              # sobrescribir sin preguntar
    "-i", input_filename,
    # Opciones de compresión:
    "-ar", "22050",    # bajar muestreo de 44100 Hz a 22050 Hz
    "-ac", "1",        # pasar a un solo canal (mono)
    "-b:a", "64k",     # bitrate de 64 kbps (la compresión se nota bastante más)
    output_filename
]
    subprocess.run(command, check=True)

    # 4. Leemos el archivo de salida como bytes
    with open(output_filename, "rb") as f:
        compressed_bytes = f.read()

    # 5. Opcional: limpiamos archivos temporales
    os.remove(input_filename)
    os.remove(output_filename)

    # 6. Devolvemos la respuesta
    return StreamingResponse(
        io.BytesIO(compressed_bytes),
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": f'attachment; filename="compressed.mp3"'
        }
    )
