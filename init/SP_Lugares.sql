-- Crear un nuevo lugar
CREATE OR REPLACE FUNCTION create_place(
    p_name VARCHAR(100),
    p_description TEXT,
    p_city VARCHAR(100),
    p_country VARCHAR(100)
) RETURNS INTEGER AS $$
DECLARE
    new_place_id INTEGER;
BEGIN
    INSERT INTO places (name, description, city, country)
    VALUES (p_name, p_description, p_city, p_country)
    RETURNING id INTO new_place_id;
    
    RETURN new_place_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener un lugar por ID
CREATE OR REPLACE FUNCTION get_place_by_id(p_place_id INTEGER)
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
    WHERE p.id = p_place_id;
END;
$$ LANGUAGE plpgsql;

-- Actualizar un lugar
CREATE OR REPLACE FUNCTION update_place(
    p_place_id INTEGER,
    p_name VARCHAR(100),
    p_description TEXT,
    p_city VARCHAR(100),
    p_country VARCHAR(100)
) RETURNS INTEGER AS $$
DECLARE
    updated_id INTEGER;
BEGIN
    UPDATE places 
    SET name = p_name, 
        description = p_description, 
        city = p_city, 
        country = p_country, 
        updated_at = CURRENT_TIMESTAMP 
    WHERE id = p_place_id 
    RETURNING id INTO updated_id;
    
    RETURN updated_id;
END;
$$ LANGUAGE plpgsql;

-- Eliminar un lugar
CREATE OR REPLACE FUNCTION delete_place(p_place_id INTEGER) RETURNS INTEGER AS $$
DECLARE
    deleted_id INTEGER;
BEGIN
    DELETE FROM places 
    WHERE id = p_place_id 
    RETURNING id INTO deleted_id;
    
    RETURN deleted_id;
END;
$$ LANGUAGE plpgsql;        

