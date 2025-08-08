from api.schemas import validate_event
from services.user_database import request_historical_user_data


def handle_user_event_logic(api_body: dict) -> dict:
    # First validate API JSON body
    validate_event(api_body)

    # Transform JSON body data
    api_body["amount"] = float(api_body["amount"])

    # Request historical user data
    user_data = request_historical_user_data(api_body["user_id"], api_body["time"], 20)

    # Perform conditional checks
    codes = conditional_checks(api_body, user_data)

    alert = len(codes) > 0
    return {
        "alert": alert,
        "codes": codes,
        "user_id": api_body["user_id"]
    }

def conditional_checks(api_body, user_data):
    codes = []

    # A withdrawal amount over 100: code 1100
    if check_amount_value(api_body):
        codes.append(1100)

    user_data.insert(0, api_body)

    # The user makes 3 consecutive withdrawals: code 30
    if check_all_transaction_types(user_data[:3], "withdraw"):
        codes.append(30)

    # The user makes 3 consecutive deposits where each one is larger than the previous
    # deposit (withdrawals in between deposits can be ignored) : code 300
    if check_increasing_types(user_data, "deposit", 3):
        codes.append(300)

    # The total amount deposited in a 30-second window exceeds 200: code 123
    if filter_time_total_amount(user_data, 30) > 200:
        codes.append(123)

    return codes


def check_amount_value(transaction: dict) -> bool:
    return transaction["amount"] > 100


def check_all_transaction_types(transactions: list[dict], transaction_type: str) -> bool:
    return all(item.get("type") == transaction_type for item in transactions)


def check_increasing_types(transactions: list[dict], transaction_type: str, limit: int) -> bool:
    count = 0
    last_amount = None

    for transaction in transactions:
        if transaction["type"] == transaction_type:
            amount = transaction["amount"]
            if last_amount is None or amount > last_amount:
                count += 1
                last_amount = amount
                if count >= limit:
                    return True
            else:
                count = 0
                last_amount = None
    return False


def filter_time_total_amount(transactions: list[dict], time_filter: int) -> float:
    time_limit = transactions[0]["time"] - time_filter
    return sum(transaction["amount"] for transaction in transactions if transaction["time"] > time_limit)
