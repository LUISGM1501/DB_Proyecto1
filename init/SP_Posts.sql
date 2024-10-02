-- Procedimiento para crear una nueva publicacion
CREATE OR REPLACE FUNCTION create_post(
    p_user_id INTEGER,
    p_content TEXT
) RETURNS INTEGER AS $$
DECLARE
    new_post_id INTEGER;
BEGIN
    INSERT INTO posts (user_id, content)
    VALUES (p_user_id, p_content)
    RETURNING id INTO new_post_id;
    
    RETURN new_post_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener una publicacion por ID
CREATE OR REPLACE FUNCTION get_post_by_id(p_post_id INTEGER)
RETURNS TABLE (
    id INTEGER,
    user_id INTEGER,
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.user_id, p.content, p.created_at, p.updated_at
    FROM posts p
    WHERE p.id = p_post_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener publicaciones paginadas
CREATE OR REPLACE FUNCTION get_posts_paginated(
    p_page INTEGER,
    p_page_size INTEGER
)
RETURNS TABLE (
    id INTEGER,
    user_id INTEGER,
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE,
    total_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    WITH posts_cte AS (
        SELECT p.*, COUNT(*) OVER() AS full_count
        FROM posts p
        ORDER BY p.created_at DESC
    )
    SELECT 
        pc.id, pc.user_id, pc.content, pc.created_at, pc.updated_at, pc.full_count
    FROM 
        posts_cte pc
    LIMIT p_page_size
    OFFSET (p_page - 1) * p_page_size;
END;
$$ LANGUAGE plpgsql;

-- Actualizar un post
CREATE OR REPLACE FUNCTION update_post(
    p_post_id INTEGER,
    p_content TEXT
) RETURNS INTEGER AS $$
DECLARE
    updated_id INTEGER;
BEGIN
    UPDATE posts 
    SET content = p_content, 
        updated_at = CURRENT_TIMESTAMP 
    WHERE id = p_post_id 
    RETURNING id INTO updated_id;
    
    RETURN updated_id;
END;
$$ LANGUAGE plpgsql;

-- Eliminar un post
CREATE OR REPLACE FUNCTION delete_post(p_post_id INTEGER) RETURNS INTEGER AS $$
DECLARE
    deleted_id INTEGER;
BEGIN
    DELETE FROM posts 
    WHERE id = p_post_id 
    RETURNING id INTO deleted_id;
    
    RETURN deleted_id;
END;
$$ LANGUAGE plpgsql;