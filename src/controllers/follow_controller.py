from config.database import get_postgres_connection
from models.user import User
from models.post import Post
from controllers import notification_controller

def follow_user(follower_id, followed_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT follow_user(%s, %s)", (follower_id, followed_id))
            new_follow_id = cur.fetchone()
            conn.commit()

            # Crear notificacion para el usuario seguido
            notification_controller.create_notification(
                followed_id,
                "follow",
                f"User {follower_id} followed you",
                None
            )

            return new_follow_id[0] if new_follow_id else None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def unfollow_user(follower_id, followed_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT unfollow_user(%s, %s)", (follower_id, followed_id))
            deleted_follow_id = cur.fetchone()
            conn.commit()
            return deleted_follow_id[0] if deleted_follow_id else None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_followed_users(user_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_followed_users(%s)", (user_id,))
            users_data = cur.fetchall()
            return [User(*user_data) for user_data in users_data]
    finally:
        conn.close()

def get_followers(user_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_followers(%s)", (user_id,))
            users_data = cur.fetchall()
            return [User(*user_data) for user_data in users_data]
    finally:
        conn.close()

def get_feed(user_id, page=1, page_size=10):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_feed(%s, %s, %s)", (user_id, page, page_size))
            posts_data = cur.fetchall()
            return [Post(*post_data) for post_data in posts_data]
    finally:
        conn.close()