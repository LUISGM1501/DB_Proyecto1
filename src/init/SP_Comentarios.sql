-- Procedimiento para crear un nuevo comentario
CREATE OR REPLACE FUNCTION create_comment(
    p_user_id INTEGER,
    p_content TEXT,
    p_post_id INTEGER DEFAULT NULL,
    p_place_id INTEGER DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    new_comment_id INTEGER;
BEGIN
    INSERT INTO comments (user_id, content, post_id, place_id)
    VALUES (p_user_id, p_content, p_post_id, p_place_id)
    RETURNING id INTO new_comment_id;
    
    RETURN new_comment_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener comentarios por post_id o place_id
CREATE OR REPLACE FUNCTION get_comments(
    p_post_id INTEGER DEFAULT NULL,
    p_place_id INTEGER DEFAULT NULL
)
RETURNS TABLE (
    id INTEGER,
    user_id INTEGER,
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.user_id, c.content, c.created_at, c.updated_at
    FROM comments c
    WHERE (p_post_id IS NOT NULL AND c.post_id = p_post_id)
       OR (p_place_id IS NOT NULL AND c.place_id = p_place_id);
END;
$$ LANGUAGE plpgsql;