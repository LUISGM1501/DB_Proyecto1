-- Procedimiento para crear un nuevo viaje
CREATE OR REPLACE FUNCTION create_trip(
    p_user_id INTEGER,
    p_title VARCHAR(200),
    p_description TEXT,
    p_start_date DATE,
    p_end_date DATE,
    p_status VARCHAR(20) DEFAULT 'planned',
    p_budget DECIMAL(10,2) DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    new_trip_id INTEGER;
BEGIN
    INSERT INTO trips (user_id, title, description, start_date, end_date, status, budget)
    VALUES (p_user_id, p_title, p_description, p_start_date, p_end_date, p_status, p_budget)
    RETURNING id INTO new_trip_id;
    
    RETURN new_trip_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener un viaje por ID
CREATE OR REPLACE FUNCTION get_trip_by_id(p_trip_id INTEGER)
RETURNS TABLE (
    id INTEGER,
    user_id INTEGER,
    title VARCHAR(200),
    description TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    budget DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT t.id, t.user_id, t.title, t.description, t.start_date, t.end_date, 
           t.status, t.budget, t.created_at, t.updated_at
    FROM trips t
    WHERE t.id = p_trip_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener viajes de un usuario
CREATE OR REPLACE FUNCTION get_user_trips(
    p_user_id INTEGER,
    p_status VARCHAR(20) DEFAULT NULL,
    p_page INTEGER DEFAULT 1,
    p_page_size INTEGER DEFAULT 10
)
RETURNS TABLE (
    id INTEGER,
    user_id INTEGER,
    title VARCHAR(200),
    description TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    budget DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE,
    total_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    WITH trips_cte AS (
        SELECT t.*, COUNT(*) OVER() AS full_count
        FROM trips t
        WHERE t.user_id = p_user_id
        AND (p_status IS NULL OR t.status = p_status)
        ORDER BY t.start_date DESC
    )
    SELECT 
        tc.id, tc.user_id, tc.title, tc.description, tc.start_date, tc.end_date,
        tc.status, tc.budget, tc.created_at, tc.updated_at, tc.full_count
    FROM trips_cte tc
    LIMIT p_page_size
    OFFSET (p_page - 1) * p_page_size;
END;
$$ LANGUAGE plpgsql;

-- Actualizar un viaje
CREATE OR REPLACE FUNCTION update_trip(
    p_trip_id INTEGER,
    p_title VARCHAR(200),
    p_description TEXT,
    p_start_date DATE,
    p_end_date DATE,
    p_status VARCHAR(20),
    p_budget DECIMAL(10,2)
) RETURNS INTEGER AS $$
DECLARE
    updated_id INTEGER;
BEGIN
    UPDATE trips 
    SET title = p_title, 
        description = p_description, 
        start_date = p_start_date,
        end_date = p_end_date,
        status = p_status,
        budget = p_budget,
        updated_at = CURRENT_TIMESTAMP 
    WHERE id = p_trip_id 
    RETURNING id INTO updated_id;
    
    RETURN updated_id;
END;
$$ LANGUAGE plpgsql;

-- Eliminar un viaje
CREATE OR REPLACE FUNCTION delete_trip(p_trip_id INTEGER) RETURNS INTEGER AS $$
DECLARE
    deleted_id INTEGER;
BEGIN
    DELETE FROM trips 
    WHERE id = p_trip_id 
    RETURNING id INTO deleted_id;
    
    RETURN deleted_id;
END;
$$ LANGUAGE plpgsql;

-- Agregar un lugar a un viaje
CREATE OR REPLACE FUNCTION add_place_to_trip(
    p_trip_id INTEGER,
    p_place_id INTEGER,
    p_visit_date DATE DEFAULT NULL,
    p_visit_order INTEGER DEFAULT NULL,
    p_notes TEXT DEFAULT NULL,
    p_rating INTEGER DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    new_entry_id INTEGER;
    next_order INTEGER;
BEGIN
    -- Si no se especifica orden, usar el siguiente disponible
    IF p_visit_order IS NULL THEN
        SELECT COALESCE(MAX(visit_order), 0) + 1 INTO next_order
        FROM trip_places 
        WHERE trip_id = p_trip_id;
    ELSE
        next_order := p_visit_order;
    END IF;

    INSERT INTO trip_places (trip_id, place_id, visit_date, visit_order, notes, rating)
    VALUES (p_trip_id, p_place_id, p_visit_date, next_order, p_notes, p_rating)
    RETURNING id INTO new_entry_id;
    
    RETURN new_entry_id;
END;
$$ LANGUAGE plpgsql;

-- Eliminar un lugar de un viaje
CREATE OR REPLACE FUNCTION remove_place_from_trip(
    p_trip_id INTEGER,
    p_place_id INTEGER
) RETURNS INTEGER AS $$
DECLARE
    deleted_entry_id INTEGER;
BEGIN
    DELETE FROM trip_places 
    WHERE trip_id = p_trip_id AND place_id = p_place_id
    RETURNING id INTO deleted_entry_id;
    
    RETURN deleted_entry_id;
END;
$$ LANGUAGE plpgsql;

-- Obtener los lugares de un viaje (ordenados por visit_order)
CREATE OR REPLACE FUNCTION get_trip_places(p_trip_id INTEGER)
RETURNS TABLE (
    place_id INTEGER,
    name VARCHAR(100),
    description TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    visit_date DATE,
    visit_order INTEGER,
    notes TEXT,
    rating INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.description, p.city, p.country,
           tp.visit_date, tp.visit_order, tp.notes, tp.rating
    FROM places p
    JOIN trip_places tp ON p.id = tp.place_id
    WHERE tp.trip_id = p_trip_id
    ORDER BY tp.visit_order ASC NULLS LAST, tp.visit_date ASC NULLS LAST;
END;
$$ LANGUAGE plpgsql;

-- Obtener estadísticas de un viaje
CREATE OR REPLACE FUNCTION get_trip_statistics(p_trip_id INTEGER)
RETURNS TABLE (
    total_places INTEGER,
    total_expenses DECIMAL(10,2),
    avg_place_rating DECIMAL(3,2),
    trip_duration_days INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*)::INTEGER FROM trip_places WHERE trip_id = p_trip_id),
        (SELECT COALESCE(SUM(amount), 0) FROM trip_expenses WHERE trip_id = p_trip_id),
        (SELECT ROUND(AVG(rating)::NUMERIC, 2) FROM trip_places WHERE trip_id = p_trip_id AND rating IS NOT NULL),
        (SELECT (t.end_date - t.start_date + 1)::INTEGER FROM trips t WHERE t.id = p_trip_id);
END;
$$ LANGUAGE plpgsql;