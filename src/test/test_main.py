from fastapi.testclient import TestClient

from src.main import app

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
