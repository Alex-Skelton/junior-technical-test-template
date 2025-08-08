from pydantic import ValidationError

from api.schemas import UserEvent, validate_event


class TestUserEventValidation:
    def test_validate_event_success(self):
        valid_data = {
            "type": "deposit",
            "amount": "42.00",
            "user_id": 2,
            "time": 1000}
        result = validate_event(valid_data)
        assert isinstance(result, UserEvent)

    def test_validate_event_invalid_type(self):
        invalid_data = {
            "type": "invalid",
            "amount": "42.00",
            "user_id": 2,
            "time": 1000
        }
        try:
            validate_event(invalid_data)
            assert False, "Expected ValidationError but got none"
        except ValidationError:
            assert True

    def test_validate_event_invalid_amount(self):
        valid_data = {
            "type": "deposit",
            "amount": 42.00,
            "user_id": 2,
            "time": 1000}
        try:
            validate_event(valid_data)
            assert False, "Expected ValidationError but got none"
        except ValidationError:
            assert True

    def test_validate_event_invalid_user_id(self):
        valid_data = {
            "type": "deposit",
            "amount": "42.0",
            "user_id": "false",
            "time": 1000}
        try:
            validate_event(valid_data)
            assert False, "Expected ValidationError but got none"
        except ValidationError:
            assert True

    def test_validate_event_invalid_time(self):
        valid_data = {
            "type": "deposit",
            "amount": "42.0",
            "user_id": 2,
            "time": "false"}
        try:
            validate_event(valid_data)
            assert False, "Expected ValidationError but got none"
        except ValidationError:
            assert True