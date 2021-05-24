import pandas as pd

from xerum.db import queries, engine


def write_to_db(df, table_name):
    """Given a DataFrame df as input, writes it to the table with name
    'table_name' using the SQLAlchemy engine defined on db.py

    Only 2 extra steps it does are:
    - Add an import timestamp
    - Lowercase column names

    Overwrites the table if it already exists

    Returns the number of rows in table 'table_name'

    """
    df = df.assign(_xerum_import_ts=pd.Timestamp.now())
    df.columns = map(str.lower, df.columns)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False, method='multi')
    return queries.row_cnt()["row_cnt"]


# TODO: enhancement
def write_to_s3(df, bucket, path):
    """Writes DataFrame df to an S3 bucket

    """
    pass
