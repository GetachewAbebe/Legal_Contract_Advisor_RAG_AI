import logging
# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Create a file handler for logging
file_handler = logging.FileHandler("log.log")
file_handler.setLevel(logging.DEBUG)
# Create a formatter and add it to the handler
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
# Add the file handler to the logger
logger.addHandler(file_handler)
