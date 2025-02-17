import logging
import structlog

def setup_logging():
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    log = structlog.get_logger()
    return log
