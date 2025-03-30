import os
import logging
from logging.handlers import RotatingFileHandler

# Configure logging directory
if not os.path.exists('../logs'):
    os.mkdir('../logs')

# Main logger setup
file_handler = RotatingFileHandler('../logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] - %(message)s'
))
file_handler.setLevel(logging.INFO)

# Error logger for severe issues
error_handler = RotatingFileHandler('../logs/error.log', maxBytes=10240, backupCount=10)
error_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] - %(message)s'
))
error_handler.setLevel(logging.ERROR)

# Performance logger
perf_handler = RotatingFileHandler('../logs/performance.log', maxBytes=10240, backupCount=5)
perf_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(message)s'
))
perf_handler.setLevel(logging.INFO)

# Set up logger instances
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(error_handler)

perf_logger = logging.getLogger('performance')
perf_logger.setLevel(logging.INFO)
perf_logger.addHandler(perf_handler)

# Make sure we don't duplicate log messages when the app imports this file
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)

if not perf_logger.handlers:
    perf_logger.addHandler(perf_handler)