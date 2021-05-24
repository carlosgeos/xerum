import os
import pytest

from xerum import app


@pytest.fixture(scope="session")
def client():
    """Main fixture.

    Creates a test client to query the API. Provides setup and
    teardown

    """
    # Setup
    with app.test_client() as client:
        yield client

    # Cleanup code
    pass


@pytest.fixture(scope="session")
def runner():
    """Flask CLI runner

    Tests can 'invoke' commands with it

    """
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def config():
    """Proxy fixture so tests can access the 'app.config' object

    """
    return app.config


@pytest.fixture(scope="session")
def init_db(runner):
    """Populate the DB with sample data

    """
    path = os.path.join(app.config["BASE_DIR"], "resources/sample-data-small.csv")
    runner.invoke(args=["load_file", path])
