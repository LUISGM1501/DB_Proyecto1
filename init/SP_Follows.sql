-- Procedimiento para seguir a un usuario
CREATE OR REPLACE FUNCTION follow_user(
    p_follower_id INTEGER,
    p_followed_id INTEGER
) RETURNS INTEGER AS $$
DECLARE
    new_follow_id INTEGER;
BEGIN
    INSERT INTO user_follows (follower_id, followed_id)
    VALUES (p_follower_id, p_followed_id)
    RETURNING id INTO new_follow_id;
    
    RETURN new_follow_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para dejar de seguir a un usuario
CREATE OR REPLACE FUNCTION unfollow_user(
    p_follower_id INTEGER,
    p_followed_id INTEGER
) RETURNS INTEGER AS $$
DECLARE
    deleted_follow_id INTEGER;
BEGIN
    DELETE FROM user_follows 
    WHERE follower_id = p_follower_id AND followed_id = p_followed_id
    RETURNING id INTO deleted_follow_id;
    
    RETURN deleted_follow_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener usuarios seguidos
CREATE OR REPLACE FUNCTION get_followed_users(p_user_id INTEGER)
RETURNS TABLE (
    id INTEGER,
    username VARCHAR(50),
    email VARCHAR(100),
    bio TEXT,
    profile_picture_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id, u.username, u.email, u.bio, u.profile_picture_url, u.created_at, u.updated_at
    FROM users u
    JOIN user_follows uf ON u.id = uf.followed_id
    WHERE uf.follower_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener seguidores
CREATE OR REPLACE FUNCTION get_followers(p_user_id INTEGER)
RETURNS TABLE (
    id INTEGER,
    username VARCHAR(50),
    email VARCHAR(100),
    bio TEXT,
    profile_picture_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id, u.username, u.email, u.bio, u.profile_picture_url, u.created_at, u.updated_at
    FROM users u
    JOIN user_follows uf ON u.id = uf.follower_id
    WHERE uf.followed_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener el feed de posts
CREATE OR REPLACE FUNCTION get_feed(
    p_user_id INTEGER,
    p_page INTEGER,
    p_page_size INTEGER
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
    SELECT p.id, p.user_id, p.content, p.created_at, p.updated_at
    FROM posts p
    JOIN user_follows uf ON p.user_id = uf.followed_id
    WHERE uf.follower_id = p_user_id
    ORDER BY p.created_at DESC
    LIMIT p_page_size
    OFFSET ((p_page - 1) * p_page_size);
END;
$$ LANGUAGE plpgsql;