-- Tabla de Viajes realizados
CREATE TABLE IF NOT EXISTS trips (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'planned' CHECK (status IN ('planned', 'in_progress', 'completed', 'cancelled')),
    budget DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector,
    CONSTRAINT valid_dates CHECK (end_date >= start_date)
);

-- Índice para búsqueda de texto completo
CREATE INDEX trips_search_idx ON trips USING GIN (search_vector);

-- Trigger para actualizar search_vector automáticamente
CREATE TRIGGER trips_search_update 
BEFORE INSERT OR UPDATE ON trips
FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', title, description);

-- Tabla de relación entre Viajes y Lugares visitados
CREATE TABLE IF NOT EXISTS trip_places (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER REFERENCES trips(id) ON DELETE CASCADE,
    place_id INTEGER REFERENCES places(id) ON DELETE CASCADE,
    visit_date DATE,
    visit_order INTEGER, -- Orden en que se visitó el lugar
    notes TEXT, -- Notas específicas de la visita a este lugar
    rating INTEGER CHECK (rating >= 1 AND rating <= 5), -- Calificación del lugar en este viaje
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(trip_id, place_id),
    UNIQUE(trip_id, visit_order) -- No puede haber dos lugares con el mismo orden en un viaje
);

-- Tabla de Gastos del Viaje (opcional, para análisis más completo)
CREATE TABLE IF NOT EXISTS trip_expenses (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER REFERENCES trips(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL, -- 'transport', 'accommodation', 'food', 'activities', 'other'
    description VARCHAR(200) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    expense_date DATE NOT NULL,
    place_id INTEGER REFERENCES places(id) ON DELETE SET NULL, -- Lugar asociado al gasto (opcional)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_trips_user_id ON trips(user_id);
CREATE INDEX idx_trips_dates ON trips(start_date, end_date);
CREATE INDEX idx_trips_status ON trips(status);
CREATE INDEX idx_trip_places_trip_id ON trip_places(trip_id);
CREATE INDEX idx_trip_places_place_id ON trip_places(place_id);
CREATE INDEX idx_trip_expenses_trip_id ON trip_expenses(trip_id);
CREATE INDEX idx_trip_expenses_date ON trip_expenses(expense_date);