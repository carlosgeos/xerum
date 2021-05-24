import sqlalchemy
import pandas as pd
from flask import request

from xerum import filestore
from xerum.util import validate, ValidationError
from xerum.db import queries
from xerum import app


@app.route("/")
def root():
    return {"ok": True}


@app.route("/balance", methods=["GET"])
def balance():
    period = request.args.get("period")
    input_doc = {"period": period}
    schema = {"period": {"allowed": ["month", "year"], "nullable": True}}
    validate(input_doc, schema)
    dispatch = {"month": queries.monthly_balance_by_account,
                "year": queries.full_balance_by_account,
                None: queries.full_balance_by_account}  # default
    res = dispatch[period]()
    return {"data": list(res)}


@app.route("/balance/account/<int:account_id>", methods=["GET"])
def balance_for_account(account_id):
    period = request.args.get("period")
    input_doc = {"account_id": account_id,
                 "period": period}
    schema = {"account_id": {"type": "integer"},
              "period": {"allowed": ["month", "year"], "nullable": True}}
    validate(input_doc, schema)
    dispatch = {"month": queries.monthly_balance_for_account,
                "year": queries.full_balance_for_account,
                None: queries.full_balance_for_account}  # default
    res = dispatch[period](account_id=account_id)
    return {"data": list(res)}


@app.route("/balance/month/<string:month>", methods=["GET"])
def balance_for_month(month):
    input_doc = {"month": month}
    schema = {"month": {"type": "string", "regex": r"^(20\d{2}-(1[0-2]|0[1-9]))"},
              "period": {"allowed": ["month", "year"], "nullable": True}}
    validate(input_doc, schema)
    res = queries.monthly_balance_for_month(month=month)
    return {"data": list(res)}


@app.route("/balance/account/<int:account_id>/month/<string:month>", methods=["GET"])
def monthly_balance_for_month_and_account(account_id, month):
    input_doc = {"month": month}
    schema = {"account_id": {"type": "integer"},
              "month": {"type": "string", "regex": r"^(20\d{2}-(1[0-2]|0[1-9]))"}}
    validate(input_doc, schema)
    res = queries.monthly_balance_for_month_and_account(account_id=account_id,
                                                        month=month)
    return {"data": res}


@app.route("/upload", methods=["POST"])
def upload():
    """CSV upload endpoint. All file extensions are allowed but an error
    will be returned if the parsing fails.

    Also checks for null or empty file names given as input

    If everything is OK, it parses and writes the file to the DB and
    returns 200

    """
    if 'file' not in request.files:
        app.logger.error("No 'file' part in form data")
        return {"error": {"msg": "No 'file' part in form data"}}, 400
    file = request.files['file']
    # if user does not select file, a client can also submit an empty
    # 'file' part without filename
    if file.filename == '':
        app.logger.error("'file' part is empty. No file name/path provided")
        return {"error": {"msg": "'file' part is empty. No file name/path provided"}}, 400
    if not file:
        app.logger.error("'file' is null")
        return {"error": {"msg": "'file' is null"}}, 400

    app.logger.info(f"Received {file}")
    # Saving the file to S3 as well would be good
    table_name = "transactions"  # fixed table name, but could be
                                 # variable as well
    df = pd.read_csv(file)
    n_rows = df.shape[0]
    app.logger.info(f"Writing {n_rows} rows to {table_name}")
    filestore.write_to_db(df, table_name)
    app.logger.info(f"Wrote dataframe to {table_name}")

    return {"file": file.filename,
            "rows_inserted": n_rows}


@app.errorhandler(ValidationError)
def validation_error(e):
    return {"error": {"msg": "Data validation error",
                      "detail": e.errors}}, 400


@app.errorhandler(pd.errors.EmptyDataError)
def empty_file_error(e):
    return {"error": {"msg": "Input file couldn't be parsed. File appears to be empty.",
                      "detail": str(e)}}, 400


@app.errorhandler(pd.errors.ParserError)
def parser_error(e):
    return {"error": {"msg": "Input file couldn't be parsed. Is it a valid CSV file ?",
                      "detail": str(e)}}, 400


@app.errorhandler(sqlalchemy.exc.ProgrammingError)
def undefined_table_error(e):
    return {"error": {"msg": "Database error. Does the 'transactions' table exist ?",
                      "detail": str(e.orig)}}, 500


@app.errorhandler(sqlalchemy.exc.OperationalError)
def database_error(e):
    return {"error": {"msg": "Database error. Is the database reachable ?",
                      "detail": str(e.orig)}}, 500


@app.errorhandler(404)
def page_not_found(error):
    return {"error": "Resource not found"}, 404
