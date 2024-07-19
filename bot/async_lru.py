from functools import wraps

def alru_cache(maxsize=128, typed=False, **kwargs):
    def decorator(func):
        cache = {}

        @wraps(func)
        async def wrapped(*args, **kwargs):
            key = args + tuple(kwargs.items())
            if key in cache:
                return cache[key]
            result = await func(*args, **kwargs)
            if len(cache) >= maxsize:
                cache.pop(next(iter(cache)))
            cache[key] = result
            return result

        return wrapped

    return decorator
    
