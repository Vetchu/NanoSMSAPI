import pytest

from src.utils.const import auth_var


@pytest.fixture
def test_input(request):
    # message = request.param.get("message", "default_message")
    # sender = request.param.get("sender", "default_sender")
    message = "bottom"
    sender = "text"
    yield {"sms": {"message": message, "sender": sender}, "auth": {"auth": auth_var}}
