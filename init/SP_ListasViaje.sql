-- Procedimiento para crear una nueva lista de viaje
CREATE OR REPLACE FUNCTION create_travel_list(
    p_user_id INTEGER,
    p_name VARCHAR(100),
    p_description TEXT
) RETURNS INTEGER AS $$
DECLARE
    new_list_id INTEGER;
BEGIN
    INSERT INTO travel_lists (user_id, name, description)
    VALUES (p_user_id, p_name, p_description)
    RETURNING id INTO new_list_id;
    
    RETURN new_list_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener una lista de viaje por ID
CREATE OR REPLACE FUNCTION get_travel_list_by_id(p_list_id INTEGER)
RETURNS TABLE (
    id INTEGER,
    user_id INTEGER,
    name VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT tl.id, tl.user_id, tl.name, tl.description, tl.created_at, tl.updated_at
    FROM travel_lists tl
    WHERE tl.id = p_list_id;
END;
$$ LANGUAGE plpgsql;

-- Actualizar una lista de viaje
CREATE OR REPLACE FUNCTION update_travel_list(
    p_list_id INTEGER,
    p_name VARCHAR(100),
    p_description TEXT
) RETURNS INTEGER AS $$
DECLARE
    updated_id INTEGER;
BEGIN
    UPDATE travel_lists 
    SET name = p_name, 
        description = p_description, 
        updated_at = CURRENT_TIMESTAMP 
    WHERE id = p_list_id 
    RETURNING id INTO updated_id;
    
    RETURN updated_id;
END;
$$ LANGUAGE plpgsql;

-- Eliminar una lista de viaje
CREATE OR REPLACE FUNCTION delete_travel_list(p_list_id INTEGER) RETURNS INTEGER AS $$
DECLARE
    deleted_id INTEGER;
BEGIN
    DELETE FROM travel_lists 
    WHERE id = p_list_id 
    RETURNING id INTO deleted_id;
    
    RETURN deleted_id;
END;
$$ LANGUAGE plpgsql;

-- Agregar un lugar a una lista de viaje
CREATE OR REPLACE FUNCTION add_place_to_list(
    p_list_id INTEGER,
    p_place_id INTEGER
) RETURNS INTEGER AS $$
DECLARE
    new_entry_id INTEGER;
BEGIN
    INSERT INTO travel_list_places (travel_list_id, place_id)
    VALUES (p_list_id, p_place_id)
    RETURNING id INTO new_entry_id;
    
    RETURN new_entry_id;
END;
$$ LANGUAGE plpgsql;

-- Eliminar un lugar de una lista de viaje
CREATE OR REPLACE FUNCTION remove_place_from_list(
    p_list_id INTEGER,
    p_place_id INTEGER
) RETURNS INTEGER AS $$
DECLARE
    deleted_entry_id INTEGER;
BEGIN
    DELETE FROM travel_list_places 
    WHERE travel_list_id = p_list_id AND place_id = p_place_id
    RETURNING id INTO deleted_entry_id;
    
    RETURN deleted_entry_id;
END;
$$ LANGUAGE plpgsql;

-- Obtener los lugares de una lista de viaje
CREATE OR REPLACE FUNCTION get_places_in_list(p_list_id INTEGER)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR(100),
    description TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.description, p.city, p.country, p.created_at, p.updated_at
    FROM places p
    JOIN travel_list_places tlp ON p.id = tlp.place_id
    WHERE tlp.travel_list_id = p_list_id;
END;
$$ LANGUAGE plpgsql;