from config.database import get_redis_connection

redis_client = get_redis_connection()

def cache_post(post_id, post_data, expire_time=3600):
    key = f"post:{post_id}"
    redis_client.setex(key, expire_time, str(post_data))

def get_cached_post(post_id):
    key = f"post:{post_id}"
    cached_post = redis_client.get(key)
    return eval(cached_post) if cached_post else None

def cache_popular_posts(posts, expire_time=3600):
    key = "popular_posts"
    redis_client.setex(key, expire_time, str(posts))

def get_cached_popular_posts():
    cached_posts = redis_client.get("popular_posts")
    return eval(cached_posts) if cached_posts else None