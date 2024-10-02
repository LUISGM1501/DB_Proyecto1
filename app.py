from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask import Flask
from dotenv import load_dotenv
from config.database import get_postgres_connection, get_mongo_connection, get_redis_connection
from routes.user_routes import user_routes
from routes.post_routes import post_routes
from routes.place_routes import place_routes
from routes.travel_list_routes import travel_list_routes
from routes.comment_routes import comment_routes
from routes.like_routes import like_routes
from routes.reaction_routes import reaction_routes
from routes.search_routes import search_routes
from routes.follow_routes import follow_routes
from routes.notification_routes import notification_routes

import os


# Cargar variables de entorno
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

# Registrar los blueprints
app.register_blueprint(user_routes)
app.register_blueprint(post_routes)
app.register_blueprint(place_routes)
app.register_blueprint(travel_list_routes)
app.register_blueprint(comment_routes)
app.register_blueprint(like_routes)
app.register_blueprint(reaction_routes)
app.register_blueprint(search_routes)
app.register_blueprint(follow_routes)
app.register_blueprint(notification_routes)

# Establecer conexiones a las bases de datos
postgres_conn = get_postgres_connection()
mongo_conn = get_mongo_connection()
redis_conn = get_redis_connection()

# Ruta de inicio
@app.route('/')
def home():
    return "Red Social de Viajes"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)