Flask para crear la API:
pip install flask


python-dotenv para manejar variables de entorno:
pip install python-dotenv


psycopg2 para conectar a PostgreSQL:
pip install psycopg2


pymongo para conectar a MongoDB:
pip install pymongo


redis para conectar a Redis:
pip install redis


Ejecutar el script dentro del contenedor
Con el contenedor corriendo, ejecutar el script para instalar las herramientas:

docker exec -it db_proyecto1-backend-1 bash
./scripts/install_tools.sh

Verifica la conexión 

Para MongoDB:
mongo --host mongodb --port 27017

Para Redis:
redis-cli -h redis -p 6379 ping

Para PostgreSQL (verificación de conexión):
ping postgres
