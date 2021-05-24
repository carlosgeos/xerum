import pugsql
import sqlalchemy

from xerum import app

engine = sqlalchemy.create_engine(app.config["DATABASE_URI"])

queries = pugsql.module(f"{app.config['BASE_DIR']}/xerum/sql/")
queries.setengine(engine)
