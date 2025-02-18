from time import time
from functools import wraps

from infra.prometheus.metrics import LLM_REQUEST_DURATION

def track_llm_duration(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time()
        try:
            result = await func(*args, **kwargs)
            duration = time() - start_time
            LLM_REQUEST_DURATION.labels(
                model='ollama',
                status='success'
            ).observe(duration)
            return result
        except Exception as e:
            duration = time() - start_time
            LLM_REQUEST_DURATION.labels(
                model='ollama',
                status='error'
            ).observe(duration)
            raise e
    return wrapper

