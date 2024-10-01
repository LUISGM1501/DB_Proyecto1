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