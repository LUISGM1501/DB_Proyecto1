from models.comment import Comment
from config.database import get_postgres_connection
from controllers import post_controller, notification_controller

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

        # Crear notificacion para el propietario del post
        if post_id:
            post = post_controller.get_post(post_id)
            if post.user_id != user_id:  # No notificar si el usuario comenta en su propio post
                notification_controller.create_notification(
                    post.user_id,
                    "comment",
                    f"User {user_id} commented on your post",
                    post_id
                )

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