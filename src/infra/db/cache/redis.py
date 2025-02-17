import aioredis


class RedisCache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(f"redis://redis:6379/")

    async def set_cache(self, key: str, value: str, expire: int = 3600):
        await self.redis.set(key, value, ex=expire)

    async def get_cache(self, key: str):
        value = await self.redis.get(key)
        return value if value else None

    async def close(self):
        await self.redis.close()

redis_cache = RedisCache()
