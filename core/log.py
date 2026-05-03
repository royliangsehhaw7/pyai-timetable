import logging
import sys

logger = logging.getLogger("timetable_generator")
logger.setLevel(logging.INFO)

# -- create a handler to stream logs to output
handler = logging.StreamHandler(sys.stdout)
# - format logger output
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# add handler to the logger
if not logger.handlers:
    logger.addHandler(handler)