import os
import pytest
import pandas as pd

from cerberus import Validator


def test_good_csv(client, config):
    with open(os.path.join(config["BASE_DIR"], "resources/sample-data-small.csv"), "rb") as f:
        res = client.post("/upload", data={"file": f})
        body = res.get_json()
        schema = {"file": {"type": "string"},
                  "rows_inserted": {"type": "integer"}}
        v = Validator(schema)
        assert v(body)
        assert res.status_code == 200


def test_good_big_csv(client, config):
    with open(os.path.join(config["BASE_DIR"], "resources/sample-data.csv"), "rb") as f:
        res = client.post("/upload", data={"file": f})
        body = res.get_json()
        schema = {"file": {"type": "string"},
                  "rows_inserted": {"type": "integer"}}
        v = Validator(schema)
        assert v(body)
        assert res.status_code == 200


def test_bad_csv(client, config):
    """Other files, such as images, should fail

    """
    with open(os.path.join(config["BASE_DIR"], "resources/dog.jpg"), "rb") as f:
        with pytest.raises(UnicodeDecodeError):
            res = client.post("/upload", data={"file": f})
            assert res.status_code == 400


def test_empty_csv(client, config):
    """An empty file should be identified as such and should return the
    corresponding message

    """
    with open(os.path.join(config["BASE_DIR"], "resources/sample-data-empty.csv"), "rb") as f:
        res = client.post("/upload", data={"file": f})
        body = res.get_json()
        schema = {"error": {"type": "dict",
                            "schema": {"detail": {"type": "string"},
                                       "msg": {"type": "string"}}}}
        v = Validator(schema)
        assert res.status_code == 400
        assert v(body)
        assert body["error"]["msg"] == "Input file couldn't be parsed. File appears to be empty."


def test_rows_csv(client, config):
    """The number of rows persisted to the database should be the same as
    the number of rows the DataFrame contains

    """
    path = os.path.join(config["BASE_DIR"], "resources/sample-data-small.csv")
    df = pd.read_csv(path)
    with open(path, "rb") as f:
        res = client.post("/upload", data={"file": f})
        body = res.get_json()
        assert body["rows_inserted"] == df.shape[0]
