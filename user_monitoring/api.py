from flask import Blueprint, current_app, request, jsonify
from pydantic import BaseModel, Field, ValidationError
from typing import Literal

from user_database.user_database import request_historical_user_data

api = Blueprint("api", __name__)

class UserEvent(BaseModel):
    """
    Pydantic model for validating incoming user event data.
    """
    type: Literal["deposit", "withdraw"] = Field(
        ..., description="The type of user action, either deposit or withdraw."
    )
    amount: str = Field(
        ..., description="The amount of money the user is depositing or withdrawing."
    )
    user_id: int = Field(
        ..., description="A unique identifier for the user."
    )
    time: int = Field(
        ..., description="The timestamp of the action (this value is always increasing)."
    )

@api.post("/event")
def handle_user_event() -> tuple:
    current_app.logger.info("Handling user event")

    api_body = request.get_json()
    if not api_body:
        current_app.logger.warning("No JSON data provided in the request body.")
        return jsonify({"message": "No input data provided"}), 400

    try:
        # Validate data
        event_data = UserEvent(**api_body)

        # If validation succeeds, event_data is now a Pydantic model instance
        # You can access its attributes directly, which also benefits from type hints
        current_app.logger.info(
            f"Validated user event: Type={event_data.type}, "
            f"Amount={event_data.amount}, UserID={event_data.user_id}, "
            f"Time={event_data.time}"
        )

        # data_validation
        # convert amount from str to float


        user_data = request_historical_user_data(api_body["user_id"], api_body["time"], 20)
        codes = conditional_checks(api_body, user_data)

        alert = True if len(codes) > 0 else False
        response_json = {
            "alert": alert,
            "codes": codes,
            "user_id": api_body["user_id"]
        }
        http_code = 200
        return response_json, http_code

    except ValidationError as e:
        # 5. Handle validation errors
        current_app.logger.error(f"Validation error for /event: {e.errors()}")
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        # 6. Catch any other unexpected errors
        current_app.logger.exception(f"An unexpected error occurred in /event: {str(e)}")
        return jsonify({"message": f"An internal server error occurred: {str(e)}"}), 500




def conditional_checks(api_body, user_data):
    codes = []

    # Code: 1100 : A withdrawal amount over 100
    if api_body["amount"] > 100:
        codes.append(1100)

    user_data.append(api_body)
    # Code: 30 : The user makes 3 consecutive withdrawals
    if check_all_transaction_types(user_data[:3], "withdraw"):
        codes.append(30)

    # Code: 300 : The user makes 3 consecutive deposits where each one is larger than the previous
    # deposit (withdrawals in between deposits can be ignored).
    if check_increasing_types(user_data, "deposit", 3):
        codes.append(300)

    # Code: 123 : The total amount deposited in a 30-second window exceeds 200
    if filter_time_total_amount(user_data, 30) > 200:
        codes.append(123)

    return codes

def check_all_transaction_types(transactions: list[dict], transaction_type) -> bool:
    return all(item.get("type") == transaction_type for item in transactions)

def check_increasing_types(transactions: list[dict], transaction_type: str, limit: int) -> bool:
    count = 0
    last_amount = transactions[0]["amount"]

    for transaction in transactions:
        if transaction["type"] == transaction_type:
            amount = transaction["amount"]
            if amount > last_amount:
                count += 1
                last_amount = amount
                if count >= limit:
                    return True
            else:
                return False
    return False

def filter_time_total_amount(transactions: list[dict], time_filter: int) -> float:
    time_limit = transactions[0]["time"] - time_filter
    return sum(transaction["amount"] for transaction in transactions if transaction["time"] > time_limit)
