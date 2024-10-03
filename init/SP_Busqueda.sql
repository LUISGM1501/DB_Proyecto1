CREATE OR REPLACE FUNCTION search_content(
    search_query TEXT,
    content_type TEXT,
    date_from TIMESTAMP WITH TIME ZONE,
    date_to TIMESTAMP WITH TIME ZONE,
    sort_by TEXT,
    sort_order TEXT,
    p_offset INTEGER,
    p_limit INTEGER
)
RETURNS TABLE (
    id INTEGER,
    result_type TEXT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    user_id INTEGER,
    username TEXT
) AS $$
DECLARE
    query_tsquery tsquery := plainto_tsquery('english', search_query);
BEGIN
    CASE
        WHEN content_type = 'post' OR content_type IS NULL THEN
            RETURN QUERY
            SELECT 
                p.id,
                'post'::TEXT AS result_type,
                LEFT(p.content, 50) AS title,
                p.content AS description,
                p.created_at,
                p.user_id,
                u.username
            FROM 
                posts p
            JOIN
                users u ON p.user_id = u.id
            WHERE 
                p.search_vector @@ query_tsquery AND
                (date_from IS NULL OR p.created_at >= date_from) AND
                (date_to IS NULL OR p.created_at <= date_to)
            ORDER BY
                CASE 
                    WHEN sort_by = 'created_at' AND sort_order = 'ASC' THEN p.created_at
                    WHEN sort_by = 'created_at' AND sort_order = 'DESC' THEN p.created_at
                    WHEN sort_by = 'title' AND sort_order = 'ASC' THEN LEFT(p.content, 50)
                    WHEN sort_by = 'title' AND sort_order = 'DESC' THEN LEFT(p.content, 50)
                END
            OFFSET p_offset
            LIMIT p_limit;

        WHEN content_type = 'place' THEN
            RETURN QUERY
            SELECT 
                pl.id,
                'place'::TEXT AS result_type,
                pl.name AS title,
                pl.description,
                pl.created_at,
                NULL::INTEGER AS user_id,
                NULL::TEXT AS username
            FROM 
                places pl
            WHERE 
                pl.search_vector @@ query_tsquery AND
                (date_from IS NULL OR pl.created_at >= date_from) AND
                (date_to IS NULL OR pl.created_at <= date_to)
            ORDER BY
                CASE 
                    WHEN sort_by = 'created_at' AND sort_order = 'ASC' THEN pl.created_at
                    WHEN sort_by = 'created_at' AND sort_order = 'DESC' THEN pl.created_at
                    WHEN sort_by = 'title' AND sort_order = 'ASC' THEN pl.name
                    WHEN sort_by = 'title' AND sort_order = 'DESC' THEN pl.name
                END
            OFFSET p_offset
            LIMIT p_limit;

        WHEN content_type = 'travel_list' THEN
            RETURN QUERY
            SELECT 
                tl.id,
                'travel_list'::TEXT AS result_type,
                tl.name AS title,
                tl.description,
                tl.created_at,
                tl.user_id,
                u.username
            FROM 
                travel_lists tl
            JOIN
                users u ON tl.user_id = u.id
            WHERE 
                tl.search_vector @@ query_tsquery AND
                (date_from IS NULL OR tl.created_at >= date_from) AND
                (date_to IS NULL OR tl.created_at <= date_to)
            ORDER BY
                CASE 
                    WHEN sort_by = 'created_at' AND sort_order = 'ASC' THEN tl.created_at
                    WHEN sort_by = 'created_at' AND sort_order = 'DESC' THEN tl.created_at
                    WHEN sort_by = 'title' AND sort_order = 'ASC' THEN tl.name
                    WHEN sort_by = 'title' AND sort_order = 'DESC' THEN tl.name
                END
            OFFSET p_offset
            LIMIT p_limit;
    END CASE;
END;
$$ LANGUAGE plpgsql;