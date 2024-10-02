from config.database import get_postgres_connection

# Crear una nueva notificación
def create_notification(user_id, type, content, related_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT create_notification(%s, %s, %s, %s)",
                (user_id, type, content, related_id)
            )
            notification_id = cur.fetchone()[0]
        conn.commit()
        return notification_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Obtener las notificaciones de un usuario
def get_user_notifications(user_id, limit=10, offset=0):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_user_notifications(%s, %s, %s)",
                (user_id, limit, offset)
            )
            notifications = cur.fetchall()
        return [
            {
                "id": row[0],
                "type": row[1],
                "content": row[2],
                "related_id": row[3],
                "is_read": row[4],
                "created_at": row[5]
            }
            for row in notifications
        ]
    finally:
        conn.close()

# Marcar una notificación como leída
def mark_notification_as_read(notification_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT mark_notification_as_read(%s)",
                (notification_id,)
            )
            success = cur.fetchone()[0]
        conn.commit()
        return success
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()