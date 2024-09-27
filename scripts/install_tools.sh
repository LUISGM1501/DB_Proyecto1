#!/bin/bash

# Actualizar los paquetes
apt-get update

# Agregar el repositorio de MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# Actualizar despues de añadir el repositorio
apt-get update

# Instalar las herramientas necesarias
apt-get install -y \
    mongodb-org-tools \
    redis-tools \
    iputils-ping

echo "Instalación de herramientas completada"
