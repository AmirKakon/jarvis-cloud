import os
import logging
from dotenv import load_dotenv

# Load the correct .env file based on the FLASK_ENV variable
if os.getenv('FLASK_ENV') == 'development':
    load_dotenv('.env.development')  # Load .env.development for development
else:
    load_dotenv('.env')  # Load .env for production

# Logging Configuration
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Set log level
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
        handlers=[
            logging.StreamHandler(),  # Console output
            logging.FileHandler("app.log", mode="a")  # Log to file
        ]
    )

# Call the setup function when this module is imported
setup_logging()

# Define other configurations
class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Load DEBUG setting from .env file
    TESTING = os.getenv('TESTING', 'False') == 'True'  # Load TESTING setting from .env file
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Load GITHUB_TOKEN from .env file
    PORT = int(os.getenv('PORT', 3000))  # Default port to 3000 if not set in .env
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')  # Default to production environment
