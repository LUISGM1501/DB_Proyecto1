from flask import Flask
from dotenv import load_dotenv
from config.database import get_postgres_connection, get_mongo_connection, get_redis_connection

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Establecer conexiones a las bases de datos
postgres_conn = get_postgres_connection()
mongo_conn = get_mongo_connection()
redis_conn = get_redis_connection()

@app.route('/')
def home():
    return "Red Social de Viajes"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
