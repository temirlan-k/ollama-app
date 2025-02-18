from prometheus_client import Counter, Gauge, Histogram

UP = Gauge("app_up", "Indicates if the application is up and running")
UP.set(1)

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"],
)

HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
)

OPERATION_COUNT = Counter(
    "operation_count_total", "Count of specific operations", ["operation_type"]
)

USER_OPERATIONS = Counter(
    "user_operations_total", "Total number of user operations", ["operation_type"]
)


LLM_REQUEST_DURATION = Histogram(
    name='llm_request_duration_seconds',
    documentation='LLM request duration ',
    labelnames=['model', 'status'],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0)
)

