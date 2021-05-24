import click
import sqlalchemy
import pandas as pd

from xerum import app
import xerum.filestore as filestore


@app.cli.command("load_file")
@click.argument("fd", type=click.File('rb'))
def load_file(fd):
    """Loads/imports a CSV file.

    FD is the file descriptor of the CSV file
    """
    app.logger.info(f"Loading file {fd}")
    table_name = "transactions"
    try:
        df = pd.read_csv(fd)
        cnt = filestore.write_to_db(df, table_name)
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as e:
        app.logger.warning("Couldn't parse CSV file")
        raise e
    except sqlalchemy.exc.SQLAlchemyError as e:
        app.logger.warning("Database error")
        raise e
    app.logger.info(f"Wrote {cnt} rows to '{table_name}'")
