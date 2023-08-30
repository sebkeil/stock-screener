import logging

# Define the format for the logging messages
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Set the basic configuration for logging
logging.basicConfig(level=logging.INFO, format=FORMAT)

# This allows you to use the configured logging when you import it from this module
logger = logging.getLogger(__name__)

