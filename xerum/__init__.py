import pugsql
from pathlib import Path
from flask import Flask

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = pugsql.module(Path(__file__).resolve().parent / "sql")
db.connect(app.config["DATABASE_URI"])

# Circular imports at the end !
import xerum.cli
import xerum.core
