from flask.testing import FlaskClient
from unittest.mock import patch


def test_handle_user_event_code_1100(client: FlaskClient) -> None:
    test_payload = {
        "type": "withdraw",
        "amount": "200.0",
        "user_id": 1,
        "time": 1000}

    fake_user_data = [
        {"type": "withdraw", "amount": 50, "time": 970},
        {"type": "deposit", "amount": 20, "time": 960},
        {"type": "deposit", "amount": 30, "time": 950}]

    with patch("services.user_service.request_historical_user_data", return_value=fake_user_data):
        response = client.post("/event", json=test_payload)
    response_data = response.json
    assert response_data["codes"] == [1100]
    assert response.status_code == 200


def test_handle_user_event_code_30(client: FlaskClient) -> None:
    test_payload = {
        "type": "withdraw",
        "amount": "100.0",
        "user_id": 1,
        "time": 1000}

    fake_user_data = [
        {"type": "withdraw", "amount": 50, "time": 970},
        {"type": "withdraw", "amount": 20, "time": 960},
        {"type": "deposit", "amount": 30, "time": 950}]

    with patch("services.user_service.request_historical_user_data", return_value=fake_user_data):
        response = client.post("/event", json=test_payload)
    response_data = response.json
    assert response_data["codes"] == [30]
    assert response.status_code == 200


def test_handle_user_event_code_300(client: FlaskClient) -> None:
    test_payload = {
        "type": "deposit",
        "amount": "10.0",
        "user_id": 1,
        "time": 1000}

    fake_user_data = [
        {"type": "deposit", "amount": 20, "time": 970},
        {"type": "withdraw", "amount": 20, "time": 960},
        {"type": "deposit", "amount": 30, "time": 950}]

    with patch("services.user_service.request_historical_user_data", return_value=fake_user_data):
        response = client.post("/event", json=test_payload)
    response_data = response.json
    assert response_data["codes"] == [300]
    assert response.status_code == 200


def test_handle_user_event_code_123(client: FlaskClient) -> None:
    test_payload = {
        "type": "deposit",
        "amount": "100.0",
        "user_id": 1,
        "time": 1000}

    fake_user_data = [
        {"type": "deposit", "amount": 110, "time": 980},
        {"type": "withdraw", "amount": 20, "time": 960},
        {"type": "deposit", "amount": 30, "time": 950}]

    with patch("services.user_service.request_historical_user_data", return_value=fake_user_data):
        response = client.post("/event", json=test_payload)
    response_data = response.json
    assert response_data["codes"] == [123]
    assert response.status_code == 200



