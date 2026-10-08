import pandas as pd


def detect_invalid_amounts(df):

    negative = (df["amount"] < 0).sum()
    zero = (df["amount"] == 0).sum()

    return {
        "negative_amounts": int(negative),
        "zero_amounts": int(zero)
    }


def clean_basic_values(df):

    df = df.copy()

    # Remove complete duplicates
    df = df.drop_duplicates()

    # Remove invalid transaction types
    valid_types = [
        "PAYMENT",
        "TRANSFER",
        "CASH_IN",
        "CASH_OUT"
    ]

    df = df[
        df["transaction_type"].isin(valid_types)
    ]

    # Convert amount to numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Remove negative amounts
    df = df[df["amount"] >= 0]

    return df