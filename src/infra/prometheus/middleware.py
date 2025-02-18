from fastapi import FastAPI
from prometheus_client import make_asgi_app
import time
from starlette.middleware.base import BaseHTTPMiddleware
from .metrics import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION,
    OPERATION_COUNT,
    UP
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            
            status_code = str(response.status_code)
            duration = time.time() - start_time
            
            HTTP_REQUESTS_TOTAL.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=status_code
            ).inc()
            
            HTTP_REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            return response
        except Exception as exc:
                HTTP_REQUESTS_TOTAL.labels(
                    method=request.method,
                    endpoint=request.url.path,
                    status_code="500"
                ).inc()
                raise exc
        

def init_prometheus(app: FastAPI):
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
    app.add_middleware(PrometheusMiddleware)
    return app

