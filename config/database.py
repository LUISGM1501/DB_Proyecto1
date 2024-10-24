import os
import psycopg2
import redis
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Configuracion de PostgreSQL
def get_postgres_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv('postgres'),  
            port=os.getenv('DB_PORT_POSTGRES'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            dbname='redsocial'
        )
        print("Conexión a PostgreSQL exitosa")
        return connection
    except Exception as e:
        print(f"Error al conectar con PostgreSQL: {e}")
        return None

# Configuracion de MongoDB
def get_mongo_connection():
    try:
        client = MongoClient(os.getenv('mongodb'), int(os.getenv('DB_PORT_MONGO'))) 
        db = client.redsocial
        print("Conexión a MongoDB exitosa")
        return db
    except Exception as e:
        print(f"Error al conectar con MongoDB: {e}")
        return None

# Configuracion de Redis
def get_redis_connection():
    try:
        redis_client = redis.Redis(
            host=os.getenv('redis'),
            port=int(os.getenv('REDIS_PORT')),
            db=0,
            decode_responses=True
        )
        print("Conexión a Redis exitosa")
        return redis_client
    except Exception as e:
        print(f"Error al conectar con Redis: {e}")
        return None
