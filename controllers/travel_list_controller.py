from models.travel_list import TravelList
from config.database import get_postgres_connection

# Crear una nueva lista de viaje
def create_travel_list(user_id, name, description):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT create_travel_list(%s, %s, %s)",
                (user_id, name, description)
            )
            list_id = cur.fetchone()[0]
        conn.commit()
        return list_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Obtener una lista de viaje por ID
def get_travel_list(list_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_travel_list_by_id(%s)", (list_id,))
            list_data = cur.fetchone()
            if list_data:
                return TravelList(*list_data)
            return None
    finally:
        conn.close()