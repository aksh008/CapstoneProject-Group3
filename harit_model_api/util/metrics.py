from functools import wraps
import time
from prometheus_client import Counter, Histogram, Info, REGISTRY, CollectorRegistry

# Create a custom registry
CUSTOM_REGISTRY = CollectorRegistry(auto_describe=True)

# Initialize metrics only once
if 'prediction_requests_total' not in REGISTRY._names_to_collectors:
    PREDICTION_REQUESTS = Counter(
        'prediction_requests_total',
        'Total number of prediction requests',
        registry=CUSTOM_REGISTRY
    )
else:
    # Get existing metric
    PREDICTION_REQUESTS = REGISTRY._names_to_collectors['prediction_requests_total']

if 'prediction_latency_seconds' not in REGISTRY._names_to_collectors:
    PREDICTION_LATENCY = Histogram(
        'prediction_latency_seconds',
        'Prediction request latency in seconds',
        registry=CUSTOM_REGISTRY
    )
else:
    PREDICTION_LATENCY = REGISTRY._names_to_collectors['prediction_latency_seconds']

if 'feedback_requests_total' not in REGISTRY._names_to_collectors:
    FEEDBACK_REQUESTS = Counter(
        'feedback_requests_total',
        'Total number of feedback submissions',
        registry=CUSTOM_REGISTRY
    )
else:
    FEEDBACK_REQUESTS = REGISTRY._names_to_collectors['feedback_requests_total']


def track_prediction_metrics(func):
    """
    Decorator to track prediction request metrics
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Increment request counter
        PREDICTION_REQUESTS.inc()

        # Track latency
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            PREDICTION_LATENCY.observe(time.time() - start_time)

    return wrapper


def setup_prometheus_metrics(app):
    """
    Additional Prometheus metric setup
    """
    # Only create info metric if it doesn't exist
    if 'ml_prediction_api' not in REGISTRY._names_to_collectors:
        info_metric = Info(
            'ml_prediction_api',
            'ML Prediction API',
            registry=CUSTOM_REGISTRY
        )
        info_metric.info({'version': '1.0'})

    # Only create requests_by_type if it doesn't exist
    if 'requests_by_type' not in REGISTRY._names_to_collectors:
        Counter(
            'requests_by_type',
            'Request count by endpoint',
            ['method'],  # Changed from labels to labelnames
            registry=CUSTOM_REGISTRY
        )