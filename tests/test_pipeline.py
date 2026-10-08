import pandas as pd

from src.cleaning import clean_basic_values
from src.validation import (
    validate_schema,
    detect_duplicates
)


def test_schema():

    df = pd.DataFrame({
        "transaction_id": ["TX1"],
        "customer_id": ["C1"],
        "amount": [100],
        "transaction_type": ["PAYMENT"],
        "merchant": ["Amazon"],
        "date": ["2026-01-01"]
    })

    result = validate_schema(df)

    assert result["schema_valid"] is True


def test_duplicate_detection():

    df = pd.DataFrame({
        "a": [1, 1, 2]
    })

    result = detect_duplicates(df)

    assert result["duplicate_count"] == 1


def test_negative_amount_removed():

    df = pd.DataFrame({
        "transaction_id": ["1", "2"],
        "customer_id": ["C1", "C2"],
        "amount": [100, -50],
        "transaction_type": [
            "PAYMENT",
            "PAYMENT"
        ],
        "merchant": [
            "Amazon",
            "Amazon"
        ],
        "date": [
            "2026-01-01",
            "2026-01-02"
        ]
    })

    clean = clean_basic_values(df)

    assert len(clean) == 1