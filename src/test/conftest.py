import pytest

from src.utils.const import auth_var


@pytest.fixture
def test_input(request):
    # message = request.param.get("message", "default_message")
    # sender = request.param.get("sender", "default_sender")
    message = "bottom"
    sender = "text"
    yield {"sms": {"message": message, "sender": sender}, "auth": {"auth": auth_var}}


# Fixture: mock insert_sms function
@pytest.fixture
def mock_insert_sms(mocker):
    mock_insert = mocker.Mock()
    mocker.patch("app.insert_sms", side_effect=mock_insert)
    return mock_insert


# Fixture: valid_auth_token
@pytest.fixture
def valid_auth_token():
    return "valid_auth_token"


# Fixture: invalid_auth_token
@pytest.fixture
def invalid_auth_token():
    return "invalid_auth_token"


# Fixture: valid_sms
@pytest.fixture
def valid_sms():
    return {"sender": "John", "message": "Hello, World!"}


# Fixture: empty_sms
@pytest.fixture
def empty_sms():
    return {}


# Fixture: auth_valid_user
@pytest.fixture
def auth_valid_user(valid_auth_token):
    return {"auth": valid_auth_token}


# Fixture: auth_invalid_user
@pytest.fixture
def auth_invalid_user(invalid_auth_token):
    return {"auth": invalid_auth_token}


# Fixture: auth_missing_token
@pytest.fixture
def auth_missing_token():
    return {}


# Fixture: auth_missing_object
@pytest.fixture
def auth_missing_object():
    return None
