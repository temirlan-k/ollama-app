import signal
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from presentation.api.v1.user import user_router
from presentation.api.v1.request import request_router
from core.di_container import DIContainer
from infra.db.mongo.db import init_mongo, close_mongo
from infra.db.redis.redis import redis_cache
import uvicorn

# Контейнер зависимостей
container = DIContainer()
container.wire(packages=['presentation.api.v1'])

@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        print("CONNECT")
        await init_mongo()  
        await redis_cache.connect()
        yield
    finally:
        print('CLOSE ALL CONNECTIONS')
        await close_mongo()  
        await redis_cache.close()

# Инициализация приложения
app = FastAPI(lifespan=lifespan)
app.container = container
app.include_router(user_router)
app.include_router(request_router)



if __name__ == "__main__":
    uvicorn.run("presentation.main:app", host="0.0.0.0", port=8888, reload=True)
