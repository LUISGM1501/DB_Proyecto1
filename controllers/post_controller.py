from models.post import Post
from config.database import get_postgres_connection
from services.cache_service import cache_post, get_cached_post

# Crear un nuevo post
def create_post(user_id, content):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT create_post(%s, %s)",
                (user_id, content)
            )
            post_id = cur.fetchone()[0]
        conn.commit()
        return post_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Obtener un post por ID
def get_post(post_id):
    cached_post = get_cached_post(post_id)
    if cached_post:
        return Post(**cached_post)

    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_post_by_id(%s)", (post_id,))
            post_data = cur.fetchone()
            if post_data:
                post = Post(*post_data)
                cache_post(post_id, post.to_dict())
                return post
            return None
    finally:
        conn.close()

# Obtener publicaciones paginadas
def get_posts_paginated(page, page_size):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_posts_paginated(%s, %s)", (page, page_size))
            posts_data = cur.fetchall()
            if posts_data:
                total_count = posts_data[0][-1]
                posts = [Post(*row[:-1]) for row in posts_data]
                return posts, total_count
            return [], 0
    finally:
        conn.close()