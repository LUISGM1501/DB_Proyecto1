-- Procedimiento para agregar un like
CREATE OR REPLACE FUNCTION add_like(
    p_user_id INTEGER,
    p_post_id INTEGER DEFAULT NULL,
    p_place_id INTEGER DEFAULT NULL
) RETURNS BOOLEAN AS $$
DECLARE
    like_exists BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM likes 
        WHERE user_id = p_user_id 
        AND (post_id = p_post_id OR place_id = p_place_id)
    ) INTO like_exists;

    IF NOT like_exists THEN
        INSERT INTO likes (user_id, post_id, place_id)
        VALUES (p_user_id, p_post_id, p_place_id);
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener el conteo de likes
CREATE OR REPLACE FUNCTION get_like_count(
    p_post_id INTEGER DEFAULT NULL,
    p_place_id INTEGER DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    like_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO like_count
    FROM likes
    WHERE (p_post_id IS NOT NULL AND post_id = p_post_id)
       OR (p_place_id IS NOT NULL AND place_id = p_place_id);
    
    RETURN like_count;
END;
$$ LANGUAGE plpgsql;