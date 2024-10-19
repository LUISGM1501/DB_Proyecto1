-- Procedimiento para crear un nuevo usuario
CREATE OR REPLACE FUNCTION create_user(
    p_username VARCHAR(50),
    p_email VARCHAR(100),
    p_password VARCHAR(255),
    p_bio TEXT,
    p_profile_picture_url VARCHAR(255)
) RETURNS INTEGER AS $$
DECLARE
    new_user_id INTEGER;
BEGIN
    INSERT INTO users (username, email, password, bio, profile_picture_url)
    VALUES (p_username, p_email, p_password, p_bio, p_profile_picture_url)
    RETURNING id INTO new_user_id;
    
    RETURN new_user_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para obtener un usuario por ID
CREATE OR REPLACE FUNCTION get_user_by_id(p_user_id INTEGER)
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
    WHERE u.id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para buscar un usuario por username
CREATE OR REPLACE FUNCTION get_user_by_username(username VARCHAR)
RETURNS TABLE (
    id INT,
    username VARCHAR,
    email VARCHAR,
    password VARCHAR,
    bio TEXT,
    profile_picture_url TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT id, username, email, password, bio, profile_picture_url, created_at, updated_at
    FROM users
    WHERE username = get_user_by_username.username;
END;
$$ LANGUAGE plpgsql;
