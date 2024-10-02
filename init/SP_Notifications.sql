CREATE OR REPLACE FUNCTION create_notification(
    p_user_id INTEGER,
    p_type VARCHAR(50),
    p_content TEXT,
    p_related_id INTEGER
) RETURNS INTEGER AS $$
DECLARE
    new_notification_id INTEGER;
BEGIN
    INSERT INTO notifications (user_id, type, content, related_id)
    VALUES (p_user_id, p_type, p_content, p_related_id)
    RETURNING id INTO new_notification_id;
    
    RETURN new_notification_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_user_notifications(
    p_user_id INTEGER,
    p_limit INTEGER DEFAULT 10,
    p_offset INTEGER DEFAULT 0
) RETURNS TABLE (
    id INTEGER,
    type VARCHAR(50),
    content TEXT,
    related_id INTEGER,
    is_read BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT n.id, n.type, n.content, n.related_id, n.is_read, n.created_at
    FROM notifications n
    WHERE n.user_id = p_user_id
    ORDER BY n.created_at DESC
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION mark_notification_as_read(
    p_notification_id INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    updated_rows INTEGER;
BEGIN
    UPDATE notifications
    SET is_read = TRUE
    WHERE id = p_notification_id;
    
    GET DIAGNOSTICS updated_rows = ROW_COUNT;
    
    RETURN updated_rows > 0;
END;
$$ LANGUAGE plpgsql;