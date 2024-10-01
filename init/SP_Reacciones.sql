-- Procedimiento para agregar o actualizar una reaccion
CREATE OR REPLACE FUNCTION add_or_update_reaction(
    p_user_id INTEGER,
    p_post_id INTEGER,
    p_reaction_type VARCHAR(20)
) RETURNS BOOLEAN AS $$
DECLARE
    reaction_exists BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM reactions 
        WHERE user_id = p_user_id AND post_id = p_post_id
    ) INTO reaction_exists;

    IF reaction_exists THEN
        UPDATE reactions
        SET reaction_type = p_reaction_type
        WHERE user_id = p_user_id AND post_id = p_post_id;
    ELSE
        INSERT INTO reactions (user_id, post_id, reaction_type)
        VALUES (p_user_id, p_post_id, p_reaction_type);
    END IF;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener el conteo de reacciones por tipo
CREATE OR REPLACE FUNCTION get_reaction_counts(p_post_id INTEGER)
RETURNS TABLE (reaction_type VARCHAR(20), count BIGINT) AS $$
BEGIN
    RETURN QUERY
    SELECT r.reaction_type, COUNT(*) as count
    FROM reactions r
    WHERE r.post_id = p_post_id
    GROUP BY r.reaction_type;
END;
$$ LANGUAGE plpgsql;