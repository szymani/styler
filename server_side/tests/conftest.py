import os
import tempfile
import pytest
from application import create_app

@pytest.fixture(scope="function")
def app():
    app = create_app(testing=True)
    client = app.test_client(use_cookies=False)
    ctx = app.test_request_context()
    ctx.push()
    yield app
    os.remove(app.config["SQLALCHEMY_DATABASE_TEST_PATH"])
    ctx.pop()

@pytest.fixture
def client(app):
    return app.test_client(use_cookies=False)


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
