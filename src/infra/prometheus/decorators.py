from functools import wraps
from prometheus_client import Counter, Histogram
import time
from typing import Callable

REQUEST_COUNT = Counter(
    'request_count_total',
    'Total count of requests by endpoint and method',
    ['endpoint', 'method']
)

REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency by endpoint and method',
    ['endpoint', 'method']
)

OPERATION_COUNT = Counter(
    'operation_count_total',
    'Count of specific operations',
    ['operation_type']
)

def track_request():
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            endpoint = func.__name__
            method = "POST" if endpoint in ["create_user", "login"] else "GET"
            
            REQUEST_COUNT.labels(endpoint=endpoint, method=method).inc()
            
            start_time = time.time()
            response = await func(*args, **kwargs)
            latency = time.time() - start_time
            REQUEST_LATENCY.labels(endpoint=endpoint, method=method).observe(latency)
            
            return response
        return wrapper
    return decorator

def track_operation(operation_type: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            OPERATION_COUNT.labels(operation_type=operation_type).inc()
            return await func(*args, **kwargs)
        return wrapper
    return decorator