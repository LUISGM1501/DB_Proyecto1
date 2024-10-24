// init/mongo/init-mongo.js
db.createUser({
    user: process.env.MONGO_INITDB_ROOT_USERNAME,
    pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
    roles: [
      {
        role: "readWrite",
        db: "redsocial"
      }
    ]
  });
  
  // Usar la base de datos redsocial
  db = db.getSiblingDB('redsocial');
  
  // Crear colecciones
  db.createCollection('travel_details');
  db.createCollection('user_stats');
  db.createCollection('activity_logs');
  db.createCollection('place_reviews');
  db.createCollection('media_links');
  
  // Crear índices
  db.travel_details.createIndex({ "user_id": 1 });
  db.travel_details.createIndex({ "created_at": -1 });
  
  db.user_stats.createIndex({ "user_id": 1 }, { unique: true });
  
  db.activity_logs.createIndex({ "user_id": 1 });
  db.activity_logs.createIndex({ "timestamp": -1 });
  
  db.place_reviews.createIndex({ "place_id": 1 });
  db.place_reviews.createIndex({ "user_id": 1 });
  db.place_reviews.createIndex({ "created_at": -1 });
  
  db.media_links.createIndex({ "reference_id": 1, "reference_type": 1 }, { unique: true });