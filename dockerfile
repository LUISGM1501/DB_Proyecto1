# Build stage
FROM python:3.9-slim as builder

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        postgresql-server-dev-all \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo los archivos necesarios para instalar dependencias
COPY requirements.txt .

# Crear y activar entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el entorno virtual del builder
COPY --from=builder /opt/venv /opt/venv

# Configurar el entorno virtual
ENV PATH="/opt/venv/bin:$PATH"

# Actualiza los paquetes e instala las herramientas necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        gnupg \
        iputils-ping \
        redis-tools \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el código fuente
COPY . .

# Exponer el puerto 5000 para Flask
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "src/app.py"]
