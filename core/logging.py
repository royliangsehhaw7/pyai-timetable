import logging
import os

def setup_logging():
    """
    Sets up the logging configuration for the application.
    Logs to console and a file.
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log")
        ]
    )
    logging.getLogger(__name__).info(f"Logging initialized with level: {log_level}")

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
