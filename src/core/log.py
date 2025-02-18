import structlog
import logging

def setup_logging()->structlog.stdlib.BoundLogger:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()  
        ],
        logger_factory=structlog.stdlib.LoggerFactory(), 
        cache_logger_on_first_use=False  
    )
    return structlog.get_logger() 

