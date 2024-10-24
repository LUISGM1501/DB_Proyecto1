from config.database import get_postgres_connection

def add_or_update_reaction(user_id, post_id, reaction_type):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT add_or_update_reaction(%s, %s, %s)",
                (user_id, post_id, reaction_type)
            )
            success = cur.fetchone()[0]
        conn.commit()
        return success
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_reaction_counts(post_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_reaction_counts(%s)", (post_id,))
            return cur.fetchall()
    finally:
        conn.close()