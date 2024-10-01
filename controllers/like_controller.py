from config.database import get_postgres_connection

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
        return success
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_like_count(post_id=None, place_id=None):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT get_like_count(%s, %s)", (post_id, place_id))
            count = cur.fetchone()[0]
        return count
    finally:
        conn.close()