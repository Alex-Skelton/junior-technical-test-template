import pytest

from services.user_service import (
    check_amount_value,
    check_all_transaction_types,
    check_increasing_types,
    filter_time_total_amount)


def test_check_amount_greater_than_true():
    transaction = {"amount": 200}
    assert check_amount_value(transaction) is True


def test_check_amount_greater_than_false():
    transaction = {"amount": 20}
    assert check_amount_value(transaction) is False


def test_check_all_transaction_types_true():
    transactions = [
        {"type": "withdraw"},
        {"type": "withdraw"},
        {"type": "withdraw"}]
    assert check_all_transaction_types(transactions, "withdraw") is True


def test_check_all_transaction_types_false():
    transactions = [
        {"type": "withdraw"},
        {"type": "deposit"},
        {"type": "withdraw"}]
    assert check_all_transaction_types(transactions, "withdraw") is False


def test_check_increasing_types_true():
    transactions = [
        {"type": "deposit", "amount": 10},
        {"type": "withdraw", "amount": 5},
        {"type": "deposit", "amount": 20},
        {"type": "deposit", "amount": 30},
        {"type": "withdraw", "amount": 500},
        {"type": "deposit", "amount": 50}]
    assert check_increasing_types(transactions, "deposit", 3) is True


def test_check_increasing_types_false():
    transactions = [
        {"type": "deposit", "amount": 10},
        {"type": "deposit", "amount": 5},
        {"type": "deposit", "amount": 15}]
    assert check_increasing_types(transactions, "deposit", 3) is False


def test_filter_time_total_amount():
    transactions = [
        {"type": "deposit", "amount": 80, "time": 100},
        {"type": "deposit", "amount": 90, "time": 95},
        {"type": "deposit", "amount": 60, "time": 91},
        {"type": "deposit", "amount": 40, "time": 50}]
    total = filter_time_total_amount(transactions, 30)
    assert total == 230
