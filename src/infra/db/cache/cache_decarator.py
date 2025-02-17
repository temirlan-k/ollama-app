import json
import hashlib
import asyncio
from functools import wraps

from pydantic import BaseModel
from infra.db.cache.redis import redis_cache

def cache_result(expire: int = 3600):

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key_data = f"{func.__name__}:{args}:{kwargs}"
            cache_key = hashlib.sha256(key_data.encode()).hexdigest()
            cached_value = await redis_cache.get_cache(cache_key)
            if cached_value:
                print("FROM CACHED VALUE")
                return json.loads(cached_value)
            result = await func(*args, **kwargs)
            if isinstance(result, list) and all(isinstance(item,BaseModel) for item in result):
                result_dict = [item.model_dump() for item in result] 
            elif isinstance(result, BaseModel):
                result_dict = result.model_dump()
            else:
                result_dict = result             
            print("FROM DB")
            await redis_cache.set_cache(cache_key, json.dumps(result_dict), expire)
            return result

        return wrapper

    return decorator
