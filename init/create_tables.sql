-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    bio TEXT,
    profile_picture_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Publicaciones
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector
);

CREATE INDEX posts_search_idx ON posts USING GIN (search_vector);

CREATE TRIGGER posts_search_update 
BEFORE INSERT OR UPDATE ON posts
FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', content);

-- Tabla de Enlaces de Media para Publicaciones
CREATE TABLE IF NOT EXISTS post_media_links (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    media_url VARCHAR(255) NOT NULL,
    media_type VARCHAR(50) NOT NULL -- e.g., 'image', 'video'
);

-- Tabla de Lugares
CREATE TABLE IF NOT EXISTS places (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector
);

CREATE INDEX places_search_idx ON places USING GIN (search_vector);

CREATE TRIGGER places_search_update 
BEFORE INSERT OR UPDATE ON places
FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', name, description, city, country);

-- Tabla de Enlaces de Imagenes para Lugares
CREATE TABLE IF NOT EXISTS place_image_links (
    id SERIAL PRIMARY KEY,
    place_id INTEGER REFERENCES places(id) ON DELETE CASCADE,
    image_url VARCHAR(255) NOT NULL
);

-- Tabla de Listas de Viaje
CREATE TABLE IF NOT EXISTS travel_lists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector
);

CREATE INDEX travel_lists_search_idx ON travel_lists USING GIN (search_vector);

CREATE TRIGGER travel_lists_search_update 
BEFORE INSERT OR UPDATE ON travel_lists
FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', name, description);

-- Tabla de Relacion entre Listas de Viaje y Lugares
CREATE TABLE IF NOT EXISTS travel_list_places (
    id SERIAL PRIMARY KEY,
    travel_list_id INTEGER REFERENCES travel_lists(id) ON DELETE CASCADE,
    place_id INTEGER REFERENCES places(id) ON DELETE CASCADE,
    UNIQUE(travel_list_id, place_id)
);

-- Tabla de Seguidores de Listas de Viaje
CREATE TABLE IF NOT EXISTS travel_list_followers (
    id SERIAL PRIMARY KEY,
    travel_list_id INTEGER REFERENCES travel_lists(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(travel_list_id, user_id)
);

-- Tabla de Comentarios (para Posts y Places)
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    place_id INTEGER REFERENCES places(id) ON DELETE CASCADE,
    CHECK (
        (post_id IS NOT NULL AND place_id IS NULL) OR
        (post_id IS NULL AND place_id IS NOT NULL)
    )
);

-- Tabla de Likes (para Posts y Places)
CREATE TABLE IF NOT EXISTS likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    place_id INTEGER REFERENCES places(id) ON DELETE CASCADE,
    CHECK (
        (post_id IS NOT NULL AND place_id IS NULL) OR
        (post_id IS NULL AND place_id IS NOT NULL)
    ),
    UNIQUE(user_id, post_id),
    UNIQUE(user_id, place_id)
);

-- Tabla de Reacciones (para Posts)
CREATE TABLE IF NOT EXISTS reactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    reaction_type VARCHAR(20) NOT NULL, -- e.g., 'like', 'love', 'haha', 'wow', 'sad', 'angry'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, post_id)
);

-- Crear extension para busqueda de texto completo si no existe
CREATE EXTENSION IF NOT EXISTS pg_trgm;


-- Tabla de Notificaciones
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- e.g., 'comment', 'like', 'follow', 'place_added'
    content TEXT NOT NULL,
    related_id INTEGER, -- ID del post, comentario, usuario o lista de viaje relacionado
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indice para mejorar el rendimiento de las consultas de notificaciones
CREATE INDEX idx_notifications_user_id ON notifications(user_id);