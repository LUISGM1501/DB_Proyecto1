# Dockerfile

# Utiliza una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Actualiza los paquetes e instala las herramientas necesarias
RUN apt-get update && \
    apt-get install -y wget gnupg iputils-ping redis-tools && \
    wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list && \
    apt-get update && \
    apt-get install -y mongodb-org-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia los archivos requeridos para el proyecto
COPY . .

# Instala las dependencias de Python necesarias
RUN pip install -r requirements.txt

# Exponer el puerto 5000 para Flask
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
