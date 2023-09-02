import pytest
from fastapi.testclient import TestClient

from src.main import app, receive_sms, HTTPException

client = TestClient(app)


def test_read_item():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello World",
    }


def test_send_sms(test_input):
    response = client.post("/sms", json=test_input)
    assert response.status_code == 200
    response_body = response.json()

    expected_value = {
        "message": test_input["sms"]["message"],
        "sender": test_input["sms"]["sender"],
    }  # Assuming you want to assert that expected_value is part of actual_value

    assert all(item in response_body.items() for item in expected_value.items())
    assert "id" in response_body


def test_get_sms():
    response = client.get("/sms")
    assert response.status_code == 200
    # assert response.json() == {
    #     "message": "Hello World",
    # }


# Test case: Valid SMS and authorized user
async def test_receive_sms_valid_sms_and_authorized_user(
        valid_sms, auth_valid_user, mock_insert_sms
):
    response = await receive_sms(valid_sms, auth_valid_user)
    assert response["id"] == "success"
    assert response["sender"] == "John"
    assert response["message"] == "Hello, World!"


# Test case: Valid SMS but unauthorized user
def test_receive_sms_valid_sms_but_unauthorized_user(valid_sms, auth_invalid_user):
    with pytest.raises(HTTPException) as exc_info:
        receive_sms(valid_sms, auth_invalid_user)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Unauthorized"


# Test case: Empty SMS
def test_receive_sms_empty_sms(empty_sms, auth_valid_user):
    with pytest.raises(HTTPException) as exc_info:
        receive_sms(empty_sms, auth_valid_user)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item not provided"


# Test case: Missing SMS
def test_receive_sms_missing_sms(auth_valid_user):
    with pytest.raises(HTTPException) as exc_info:
        receive_sms(None, auth_valid_user)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item not provided"


# Test case: Valid SMS and authorized user, but insert fails
@pytest.mark.asyncio
async def test_receive_sms_valid_sms_and_authorized_user_insert_fails(
        valid_sms, auth_valid_user, mock_insert_sms
):
    mock_insert_sms.return_value = "failure"
    response = await receive_sms(valid_sms, auth_valid_user)
    assert response["id"] == "failure"
    assert response["sender"] == "John"
    assert response["message"] == "Hello, World!"


# Test case: Valid SMS and authorized user, but insert throws an exception
def test_receive_sms_valid_sms_and_authorized_user_insert_exception(
        valid_sms, auth_valid_user, mock_insert_sms
):
    mock_insert_sms.side_effect = Exception()
    with pytest.raises(Exception):
        receive_sms(valid_sms, auth_valid_user)


# Test case: Valid SMS and authorized user, but invalid session
def test_receive_sms_valid_sms_and_authorized_user_invalid_session(
        valid_sms, auth_valid_user
):
    with pytest.raises(Exception):
        receive_sms(valid_sms, auth_valid_user)


# Test case: Valid SMS and authorized user, but invalid auth token
def test_receive_sms_valid_sms_and_authorized_user_invalid_auth_token(
        valid_sms, auth_missing_token
):
    with pytest.raises(Exception):
        receive_sms(valid_sms, auth_missing_token)


# Test case: Valid SMS and authorized user, but missing auth token
def test_receive_sms_valid_sms_and_authorized_user_missing_auth_token(
        valid_sms, auth_missing_token
):
    with pytest.raises(Exception):
        receive_sms(valid_sms, auth_missing_token)


# Test case: Valid SMS and authorized user, but missing auth object
def test_receive_sms_valid_sms_and_authorized_user_missing_auth_object(
        valid_sms, auth_missing_object
):
    with pytest.raises(Exception):
        receive_sms(valid_sms, auth_missing_object)
