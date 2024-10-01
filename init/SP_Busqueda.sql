CREATE OR REPLACE FUNCTION search_content(search_query TEXT)
RETURNS TABLE (
    id INTEGER,
    content_type TEXT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    (SELECT 
        p.id,
        'post' AS content_type,
        LEFT(p.content, 50) AS title,
        p.content AS description,
        p.created_at
    FROM 
        posts p
    WHERE 
        p.content ILIKE '%' || search_query || '%')
    UNION ALL
    (SELECT 
        pl.id,
        'place' AS content_type,
        pl.name AS title,
        pl.description,
        pl.created_at
    FROM 
        places pl
    WHERE 
        pl.name ILIKE '%' || search_query || '%' OR
        pl.description ILIKE '%' || search_query || '%')
    UNION ALL
    (SELECT 
        tl.id,
        'travel_list' AS content_type,
        tl.name AS title,
        tl.description,
        tl.created_at
    FROM 
        travel_lists tl
    WHERE 
        tl.name ILIKE '%' || search_query || '%' OR
        tl.description ILIKE '%' || search_query || '%')
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;