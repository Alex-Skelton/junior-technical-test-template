import random


def request_historical_user_data(user_id, time, records):
    # Setup fake function that requests data from database service
    # Realistically this could be an API request to another service, a database on the same server or a data stream like kafka
    data = generate_random_transactions(
        user_id=user_id,
        time=time,
        num_items=records)
    return data


def generate_random_transactions(
    num_items: int,
    user_id: int,
    time: int,
    min_amount: float = 1.00,
    max_amount: float = 1000.00,
    transaction_types: list[str] = None,
) -> list[dict]:
    # A function that generates a list of dictionaries containing historical user data,
    if num_items <= 0:
        return []

    if transaction_types is None:
        transaction_types = ["deposit", "withdraw"]

    transactions = []
    for i in range(num_items):
        amount = round(random.uniform(min_amount, max_amount), 2)
        transaction_type = random.choice(transaction_types)
        time = time - random.randint(1, 10000)
        transaction = {
            "user_id": user_id,
            "amount": amount,
            "type": transaction_type,
            "time": time}
        transactions.append(transaction)
    return transactions



#
# # 1. Generate 5 random transactions
# print("--- 5 Random Transactions ---")
# my_transactions = generate_random_transactions(num_items=5, user_id=5)
# for t in my_transactions:
#     print(t)
# print("\n")
#
# # 2. Generate 10 transactions with custom starting IDs and amounts
# print("--- 10 Custom Transactions ---")
# custom_transactions = generate_random_transactions(
#     num_items=10,
#     user_id=100,
#     start_transaction_id=5000,
#     min_amount=10.00,
#     max_amount=500.00
# )
# for t in custom_transactions:
#     print(t)
# print("\n")
#
# # 3. Generate 3 transactions with only "deposit" type
# print("--- 3 Deposit-Only Transactions ---")
# deposit_only = generate_random_transactions(
#     num_items=3,
#     transaction_types=["deposit"]
# )
# for t in deposit_only:
#     print(t)
# print("\n")
#
# # 4. Generate 0 transactions (should return an empty list)
# print("--- 0 Transactions ---")
# empty_list = generate_random_transactions(num_items=0)
# print(empty_list)