# Usa Python 3.9 slim (o la versión que prefieras)
FROM python:3.9-slim

# Actualizamos e instalamos ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Creamos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos requirements e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Exponemos el puerto 8000
EXPOSE 8000

# Comando para iniciar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
