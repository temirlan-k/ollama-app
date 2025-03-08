from contextlib import asynccontextmanager

from fastapi import FastAPI

from bootstrap.di_container import container
from infra.db.cache.redis import redis_cache
from infra.db.mongo_db.db import close_mongo, init_mongo
from infra.prometheus.middleware import init_prometheus
from infra.sentry.sentry import init_sentry
from presentation.api.rest.v1.request import request_router
from presentation.api.rest.v1.user import user_router
from presentation.api.rest.v1.analytics import analytics_router
from presentation.api.graphql import graphql_app




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
    init_sentry()
    app = FastAPI(lifespan=lifespan)
    app.container = container
    app.include_router(user_router)
    app.include_router(request_router)
    app.include_router(analytics_router)
    app.include_router(graphql_app,prefix='/graphql')
    init_prometheus(app)
    return app



app = create_app()



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("bootstrap.main:app", host="0.0.0.0", port=8888, reload=True)
