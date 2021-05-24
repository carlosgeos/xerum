import os
import pytest


def test_good_csv_cli(runner, config):
    """A valid CSV returns a success exit code

    """
    path = os.path.join(config["BASE_DIR"], "resources/sample-data-small.csv")
    res = runner.invoke(args=["load_file", path])
    assert res.exit_code == 0


def test_bad_csv_cli(runner, config):
    """A non-CSV file must fail

    """
    path = os.path.join(config["BASE_DIR"], "resources/dog.jpg")
    with pytest.raises(UnicodeDecodeError):
        res = runner.invoke(args=["load_file", path])
        assert res.exit_code == 1
        raise res.exception


def test_missing_file_cli(runner, config):
    """A missing required argument should display some information about
    the problem to users and fail with exit code = 2

    """
    res = runner.invoke(args=["load_file"])
    assert "Missing argument 'FD'" in res.output
    assert res.exit_code == 2        # Exit code 2 = shell misuse
