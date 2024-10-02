from config.database import get_postgres_connection
from controllers import post_controller, notification_controller

# Agregar un like a un post o lugar
def add_like(user_id, post_id=None, place_id=None):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT add_like(%s, %s, %s)",
                (user_id, post_id, place_id)
            )
            success = cur.fetchone()[0]
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

        return success
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Obtener el número de likes de un post o lugar
def get_like_count(post_id=None, place_id=None):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT get_like_count(%s, %s)", (post_id, place_id))
            count = cur.fetchone()[0]
        return count
    finally:
        conn.close()