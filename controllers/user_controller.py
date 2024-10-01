from models.user import User
from config.database import get_postgres_connection

# Crear un nuevo usuario
def create_user(username, email, password, bio=None, profile_picture_url=None):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(

                "SELECT create_user(%s, %s, %s, %s, %s)",
                (username, email, password, bio, profile_picture_url)
            )
            user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Obtener un usuario por ID
def get_user(user_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_user_by_id(%s)", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                return User(*user_data)
            return None
    finally:
        conn.close()