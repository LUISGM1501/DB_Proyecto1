# middleware/rate_limit.py
from functools import wraps
from flask import request, jsonify
from services.cache_manager import CacheManager

cache_manager = CacheManager()

def rate_limit(limit=100, window=3600):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Obtener identificador de usuario o IP
            user_id = getattr(getattr(request, 'user', None), 'id', None)
            if not user_id:
                user_id = request.remote_addr

            # Obtener el nombre de la acción del endpoint
            action = request.endpoint

            # Verificar el rate limit
            if not cache_manager.check_rate_limit(user_id, action, limit):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Please try again after some time'
                }), 429

            return f(*args, **kwargs)
        return decorated_function
    return decorator