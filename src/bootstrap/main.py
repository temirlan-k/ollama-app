from contextlib import asynccontextmanager

from fastapi import FastAPI

from bootstrap.di_container import DIContainer
from infra.db.cache.redis import redis_cache
from infra.db.mongo_db.db import close_mongo, init_mongo
from infra.prometheus.middleware import init_prometheus
from presentation.api.v1.request import request_router
from presentation.api.v1.user import user_router

container = DIContainer()
container.wire(packages=["presentation.api.v1"])


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        await init_mongo()
        await redis_cache.connect()
        yield
    finally:
        await close_mongo()
        await redis_cache.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.container = container
    app.include_router(user_router)
    app.include_router(request_router)
    init_prometheus(app)
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("presentation.main:app", host="0.0.0.0", port=8888, reload=True)
