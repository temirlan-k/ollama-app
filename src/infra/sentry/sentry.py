import sentry_sdk

sentry_sdk.init(
    dsn="https://7579c4cf2468d9d07efe442e73387cde@o4508901639520256.ingest.de.sentry.io/4508901643518032",
    send_default_pii=True,
    traces_sample_rate=1.0,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)