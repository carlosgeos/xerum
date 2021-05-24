import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database config. The default URI string is valid for the docker
# container. Could also be a SQLite database
DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://postgres:postgres@postgres/postgres")
DATABASE_CONNECT_OPTIONS = {}
