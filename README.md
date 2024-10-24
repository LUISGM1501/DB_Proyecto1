# Red Social de Viajes

Este proyecto es el backend de una red social orientada a compartir experiencias de viaje, utilizando Flask para la API, PostgreSQL, MongoDB y Redis como bases de datos, y desplegado mediante Docker.

## 1. Descripción General

El sistema permite a los usuarios realizar publicaciones sobre viajes, interactuar con otros mediante comentarios, likes, y gestionar listas de destinos turísticos. Todo el backend está contenido en Docker para facilitar el despliegue y replicación.

El proyecto se basa en tres tecnologías principales de bases de datos:

- PostgreSQL para la gestión de datos estructurados (usuarios, publicaciones, etc.).
- MongoDB para almacenamiento no estructurado o semi-estructurado (por ejemplo, listas de viajes).
- Redis como caché para optimizar la carga de publicaciones populares y gestionar sesiones.

## 2. Requisitos del Proyecto

### Tecnologías Utilizadas

- Flask para crear la API web:
  ```bash
  pip install flask
  ```

- python-dotenv para manejar variables de entorno:
  ```bash
  pip install python-dotenv
  ```

- psycopg2 para conectar a PostgreSQL:
  ```bash
  pip install psycopg2
  ```

- pymongo para conectar a MongoDB:
  ```bash
  pip install pymongo
  ```

- redis para conectar a Redis:
  ```bash
  pip install redis
  ```

### Otras dependencias
- pytest y pytest-cov para pruebas unitarias e integración.

## 3. Instrucciones de Instalación y Ejecución

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/LUISGM1501/DB_Proyecto1.git
   cd DB_Proyecto1
   ```

2. Configurar el entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/MacOS
   venv\Scripts\activate     # En Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar las variables de entorno: 
   Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   ```

5. Desplegar con Docker:
   Asegúrate de tener Docker y Docker Compose instalados, luego ejecuta:
   ```bash
   docker-compose up --build
   ```

6. Ejecutar el script dentro del contenedor:
   Con el contenedor corriendo, ejecuta el script para instalar herramientas:
   ```bash
   docker exec -it db_proyecto1-backend-1 bash
   ./scripts/install_tools.sh
   ```

## 4. Verificación de Conexiones de Base de Datos

Una vez que el contenedor está corriendo, puedes verificar la conexión con las bases de datos:

- MongoDB:
  ```bash
  mongo --host mongodb --port 27017
  ```

- Redis:
  ```bash
  redis-cli -h redis -p 6379 ping
  ```

- PostgreSQL:
  ```bash
  ping postgres
  ```

## 5. Estructura del Proyecto

## 6. Documentación de MongoDB en la Red Social de Viajes

### 6.1 Justificación de Uso
MongoDB fue seleccionado para almacenar ciertos tipos de datos en nuestra aplicación por las siguientes razones:

#### 6.1.1 Datos Flexibles y Dinámicos
- Detalles de Viajes: La información de viajes puede variar significativamente entre usuarios. MongoDB permite almacenar datos con estructura flexible sin necesidad de modificar el esquema.
- Reseñas de Lugares: Las reseñas pueden incluir diferentes tipos de contenido y metadatos que serían complejos de manejar en una base de datos relacional.
1.2 Consultas Eficientes
- Logs de Actividad: MongoDB es eficiente para escribir y consultar grandes volúmenes de datos de registro.
- Media Links: Facilita el almacenamiento y recuperación de colecciones de enlaces multimedia.
#### 6.1.3 Escalabilidad
- Permite escalar horizontalmente para manejar grandes volúmenes de datos.
- Proporciona índices eficientes para consultas frecuentes.

### 6.2 Estructura de Datos

#### 6.2.1 Colecciones

**travel_details**
```json
{
  _id: ObjectId,
  user_id: Int,
  title: String,
  description: String,
  places: Array[{
    id: Int,
    name: String,
    coordinates: {
      lat: Float,
      lng: Float
    }
  }],
  start_date: Date,
  end_date: Date,
  budget: {
    currency: String,
    amount: Float
  },
  expenses: Array[{
    category: String,
    amount: Float,
    description: String
  }],
  itinerary: Array[{
    day: Int,
    activities: Array[String]
  }],
  tips: Array[String],
  photos: Array[String],
  created_at: Date
}
```

**user_stats**
```json
{
  _id: ObjectId,
  user_id: Int,
  total_posts: Int,
  total_likes_received: Int,
  total_comments_received: Int,
  places_visited: Array[Int],
  countries_visited: Array[String],
  created_at: Date,
  last_updated: Date
}
```

**activity_logs**
```json
{
  _id: ObjectId,
  user_id: Int,
  activity_type: String,
  details: Object,
  timestamp: Date
}
```

**place_reviews**
```json
{
  _id: ObjectId,
  place_id: Int,
  user_id: Int,
  rating: Int,
  detailed_text: String,
  visit_date: Date,
  recommendations: Array[String],
  tips: Array[String],
  photos: Array[String],
  categories: Array[String],
  price_level: Int,
  visited_with: String,
  highlights: Array[String],
  created_at: Date,
  updated_at: Date
}
```

**media_links**
```json
{
  _id: ObjectId,
  reference_id: Int,
  reference_type: String,
  links: Array[{
    url: String,
    type: String,
    description: String
  }],
  created_at: Date
}
```

#### 6.2.3 Índices
Se han creado los siguientes índices para optimizar las consultas más frecuentes:

**travel_details**
```bash
db.travel_details.createIndex({ "user_id": 1 })
db.travel_details.createIndex({ "created_at": -1 })
```

**user_stats**
```bash
db.user_stats.createIndex({ "user_id": 1 }, { unique: true })
```

**activity_logs**
db.activity_logs.createIndex({ "user_id": 1 })
db.activity_logs.createIndex({ "timestamp": -1 })

**place_reviews**
```bash
db.place_reviews.createIndex({ "place_id": 1 })
db.place_reviews.createIndex({ "user_id": 1 })
db.place_reviews.createIndex({ "created_at": -1 })

**media_links**
```bash
db.media_links.createIndex({ "reference_id": 1, "reference_type": 1 }, { unique: true })
```

## 7. Integración con PostgreSQL
MongoDB complementa a PostgreSQL de la siguiente manera:

- PostgreSQL: Almacena datos estructurados y relacionales como usuarios, lugares básicos, y relaciones entre entidades.
- MongoDB: Almacena datos semi-estructurados y detalles extensos que requieren flexibilidad.

## 8. Modelo de datos 

![Modelo de datos](./Imagenes/ModeloDatos.png)

### 8.1. Modelo de datos en PostgreSQL

![Modelo de datos en PostgreSQL](./Imagenes/PostgreSQL.png)

### 8.2. Modelo de datos en MongoDB

![Modelo de datos en MongoDB](./Imagenes/MongoDB.png)

### 8.3. Modelo de datos en Redis

![Modelo de datos en Redis](./Imagenes/Redis.png)
