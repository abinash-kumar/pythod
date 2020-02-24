import logging
# import logging.handlers
from django.conf import settings

LOG_FILENAME = settings.LOG_DIR

# Set up a specific logger with our desired output level
ab_logger = logging.getLogger('MyLogger')
# ab_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20000, backupCount=50)
ab_logger.addHandler(handler)
