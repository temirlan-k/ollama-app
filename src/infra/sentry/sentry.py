import os
import sentry_sdk


def init_sentry():
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        send_default_pii=True,
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )