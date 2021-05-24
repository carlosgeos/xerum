# [Xerum](https://xerum.herokuapp.com)

A (cheap) Xero clone.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/carlosgeos/xerum)

## Usage

```
$ docker-compose up
```

The API will be available at `http://localhost:5000`

## Test

Once the service is up and running:
```
$ docker-compose exec xerum python -m pytest

...

===================================== test session starts =====================================
platform linux -- Python 3.9.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /app
plugins: hypothesis-6.13.5
collected 13 items

tests/test_balance.py .....
tests/test_cli.py ...
tests/test_file_upload.py .....

===================================== 13 passed in 6.93s ======================================
```

## Deploy

Simply push it to Heroku. `heroku.yml` makes Heroku build the image
automatically and run the container with the correct config. Only the
ENV var `DATABASE_URI` is needed.

App is containerized so it can be deployed virtually anywhere.

## API docs

#### Load CSV file to the database.

#### Option 1
Submit the file on the `file` key of a POST form to `/upload`.

*Example:*
```sh
$ curl -F 'file=@./resources/sample-data.csv' http://localhost:5000/upload

...

{
  "file": "sample-data.csv",
  "rows_inserted": 79999
}
```
The same can be easily achieved with Postman as well.

#### Option 2

Using the CLI:
```sh
$ docker-compose exec <service> flask load_file <file>
```

*Example:*
```sh
$ docker-compose exec xerum flask load_file resources/sample-data-small.csv

...

[2021-05-26 13:23:40,271] INFO in cli: Loading file <_io.BufferedReader name='resources/sample-data-small.csv'>
[2021-05-26 13:23:40,382] INFO in cli: Wrote 500 rows to 'transactions'
```

CLI help is available for this command using:
```sh
$ docker-compose exec xerum flask load_file help

>>> Usage: flask load_file [OPTIONS] FD

  Loads/imports a CSV file.

  FD is the file descriptor of the CSV file

Options:
  --help  Show this message and exit.
```


#### Get the yearly balances, sliced by account
```sh
$ curl -X GET -H "Content-type: application/json" 'http://localhost:5000/balance'
```

Optionally, the query arg `?period=year` can be passed, though yearly balances are the default.

#### Get yearly balances for a specific account
```sh
$ curl -X GET -H "Content-type: application/json" 'http://localhost:5000/balance/account/<account_id>'
```

Optionally, the query arg `?period=year` can be passed, though yearly balances are the default.

#### Get monthly balances, sliced by account
```sh
$ curl -X GET -H "Content-type: application/json" 'http://localhost:5000/balance?period=month'
```


#### Get monthly balances for a specific account
```sh
$ curl -X GET -H "Content-type: application/json" 'http://localhost:5000/balance/account/<account_id>?period=month'
```


#### Get the monthly balance for a specific month, sliced by account
```sh
$ curl -X GET -H "Content-type: application/json" 'http://localhost:5000/balance/month/<YYYY-MM>'
```


#### Get the monthly balance for a specific month and a specific account
```sh
$ curl -X GET -H "Content-type: application/json" 'http://localhost:5000/balance/account/<account_id>/month/<YYYY-MM>'
```


## Rationale and design

### DB / ORM

The persistence layer uses PostgreSQL, but could use anything if the
SQL is adapted.

There is no ORM. SQL is written using PugSQL.

Data loads/imports are handled by Pandas (`.to_sql()`), but using
Postgres' `COPY` command would be a lot faster for huge CSV files.

### Logging

Xerum uses the standard Python/Flask app `logging` module. It logs to
`stdout`.

### Testing

`pytest` is the test runner.

Hypothesis provides some property-based/generative testing as well.

### Data validation

Data and input validation is done by Cerberus. If any handler receives
disallowed data, the `validate` function will raise a
`ValidationError`, which will in turn make the API explain what the
error was.

## Limitations

The `transactions` table is assumed to have the following DDL:

```sql
create table transactions
(
    date             text,
    account          bigint,
    amount           double precision,
    _xerum_import_ts timestamp
);
```

Pandas automatically creates this table (`/upload` endpoint) and adds
the timestamp, if it is given a CSV file with the same first three
columns.
