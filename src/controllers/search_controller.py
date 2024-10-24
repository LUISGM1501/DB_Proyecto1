from config.database import get_postgres_connection

def search_content(query):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_content(%s)", (query,))
            results = cur.fetchall()
            return [
                {
                    "id": row[0],
                    "content_type": row[1],
                    "title": row[2],
                    "description": row[3],
                    "created_at": row[4]
                }
                for row in results
            ]
    finally:
        conn.close()