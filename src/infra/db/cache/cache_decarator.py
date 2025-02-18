import json
import hashlib
from functools import wraps
from pydantic import BaseModel
from infra.db.cache.redis import redis_cache
from core.log import setup_logging

logger = setup_logging()


def cache_result(expire: int = 3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key_data = f"{func.__name__}:{args}:{kwargs}"
            cache_key = hashlib.sha256(key_data.encode()).hexdigest()

            try:
                cached_value = await redis_cache.get_cache(cache_key)
                if cached_value:
                    logger.info(f"Cache hit for {cache_key}. Fetched from RedisCache")
                    return json.loads(cached_value)
            except Exception as e:
                logger.error(f"Error getting cache for {cache_key}: {e}")

            result = await func(*args, **kwargs)

            if isinstance(result, list) and all(
                isinstance(item, BaseModel) for item in result
            ):
                result_dict = [item.model_dump() for item in result]
            elif isinstance(result, BaseModel):
                result_dict = result.model_dump()
            else:
                result_dict = result

            try:
                await redis_cache.set_cache(cache_key, json.dumps(result_dict), expire)
                logger.info(f"Cache set for {cache_key}. Fetched from DB")
            except Exception as e:
                logger.error(f"Error setting cache for {cache_key}: {e}")

            return result

        return wrapper

    return decorator
