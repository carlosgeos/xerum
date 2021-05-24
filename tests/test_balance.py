from cerberus import Validator
from hypothesis import given, strategies as st


yearly_balance_schema = {"type": "dict",
                         "schema": {"account": {"type": "integer"},
                                    "balance": {"type": "number"},
                                    "year": {"type": "integer",
                                             "min": 2000,
                                             "max": 2099}}}


monthly_balance_schema = {"type": "dict",
                          "schema": {"account": {"type": "integer"},
                                     "balance": {"type": "number"},
                                     "month": {"type": "string",
                                               "regex": r"^(20\d{2}-(1[0-2]|0[1-9]))"}}}


def test_healthcheck(client):
    res = client.get("/")
    assert res.status_code == 200


def test_balance(client, init_db, config):
    """Yearly balances should return a 200 HTTP code and data should match
    the schema

    """

    res = client.get("/balance")
    body = res.get_json()
    schema = {"data": {"type": "list",
                       "schema": yearly_balance_schema,
                       "empty": True}}
    v = Validator(schema)
    assert v(body)
    assert res.status_code == 200


@given(period=st.text().filter(lambda x: x not in ["year", "month"]))
def test_balance_wrong_period(client, init_db, config, period):
    """A 'period' query arg other than year or month should fail

    """
    res = client.get("/balance", query_string={"period": period})
    body = res.get_json()
    assert res.status_code == 400
    assert body["error"]["msg"] == "Data validation error"


def test_balance_monthly(client, init_db, config):
    """Monthly balances should return a 200 HTTP code and data should
    match the schema

    """
    res = client.get("/balance", query_string={"period": "month"})
    body = res.get_json()
    schema = {"data": {"type": "list",
                       "schema": monthly_balance_schema,
                       "empty": True}}
    v = Validator(schema)
    assert res.status_code == 200
    assert v(body)


@given(month=st.from_regex(r"^(20\d{2}-(1[0-2]|0[1-9]))", fullmatch=True))
def test_balance_for_month(client, init_db, config, month):
    """Month-specific balances should return a 200 HTTP code and data
    should match the schema

    """
    res = client.get(f"/balance/month/{month}")
    body = res.get_json()
    schema = {"data": {"type": "list",
                       "schema": monthly_balance_schema,
                       "empty": True}}
    v = Validator(schema)
    assert res.status_code == 200
    assert v(body)
