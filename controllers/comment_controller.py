from models.comment import Comment
from config.database import get_postgres_connection

# Crear un nuevo comentario 
def create_comment(user_id, content, post_id=None, place_id=None):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT create_comment(%s, %s, %s, %s)",
                (user_id, content, post_id, place_id)
            )
            comment_id = cur.fetchone()[0]
        conn.commit()
        return comment_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Obtener comentarios de un post o lugar
def get_comments(post_id=None, place_id=None):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_comments(%s, %s)", (post_id, place_id))
            comments_data = cur.fetchall()
            return [Comment(*comment_data) for comment_data in comments_data]
    finally:
        conn.close()