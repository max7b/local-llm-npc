import logging

# Create a custom logger
LOGGING = logging.getLogger(__name__)

# Configure the logger to log to the terminal
handler = logging.StreamHandler()
formatter = logging.Formatter("--- %(asctime)s - %(levelname)s ---\n%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

# Add the handler to the logger
LOGGING.addHandler(handler)

# Set the logging level (optional, default is DEBUG)
LOGGING.setLevel(logging.DEBUG)
