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

Instala coverage y pytest-cov para generar reportes de cobertura de código:
pip install coverage pytest-cov


# Documentación de MongoDB en la Red Social de Viajes

## 1. Justificación de Uso

MongoDB fue seleccionado para almacenar ciertos tipos de datos en nuestra aplicación por las siguientes razones:

### 1.1 Datos Flexibles y Dinámicos
- **Detalles de Viajes**: La información de viajes puede variar significativamente entre usuarios. MongoDB permite almacenar datos con estructura flexible sin necesidad de modificar el esquema.
- **Reseñas de Lugares**: Las reseñas pueden incluir diferentes tipos de contenido y metadatos que serían complejos de manejar en una base de datos relacional.

### 1.2 Consultas Eficientes
- **Logs de Actividad**: MongoDB es eficiente para escribir y consultar grandes volúmenes de datos de registro.
- **Media Links**: Facilita el almacenamiento y recuperación de colecciones de enlaces multimedia.

### 1.3 Escalabilidad
- Permite escalar horizontalmente para manejar grandes volúmenes de datos.
- Proporciona índices eficientes para consultas frecuentes.

## 2. Estructura de Datos

### 2.1 Colecciones

#### travel_details
```javascript
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

#### user_stats
```javascript
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

#### activity_logs
```javascript
{
  _id: ObjectId,
  user_id: Int,
  activity_type: String,
  details: Object,
  timestamp: Date
}
```

#### place_reviews
```javascript
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

#### media_links
```javascript
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

## 3. Índices

Se han creado los siguientes índices para optimizar las consultas más frecuentes:

```javascript
// travel_details
db.travel_details.createIndex({ "user_id": 1 })
db.travel_details.createIndex({ "created_at": -1 })

// user_stats
db.user_stats.createIndex({ "user_id": 1 }, { unique: true })

// activity_logs
db.activity_logs.createIndex({ "user_id": 1 })
db.activity_logs.createIndex({ "timestamp": -1 })

// place_reviews
db.place_reviews.createIndex({ "place_id": 1 })
db.place_reviews.createIndex({ "user_id": 1 })
db.place_reviews.createIndex({ "created_at": -1 })

// media_links
db.media_links.createIndex({ "reference_id": 1, "reference_type": 1 }, { unique: true })
```

## 4. Integración con PostgreSQL

MongoDB complementa a PostgreSQL de la siguiente manera:

- **PostgreSQL**: Almacena datos estructurados y relacionales como usuarios, lugares básicos, y relaciones entre entidades.
- **MongoDB**: Almacena datos semi-estructurados y detalles extensos que requieren flexibilidad.

## 5. Mantenimiento y Backup

- Se recomienda realizar backups diarios de las colecciones de MongoDB.
- Los índices deben ser revisados y optimizados periódicamente.
- Monitorear el crecimiento de las colecciones, especialmente activity_logs.