import pandas as pd
from src.ingestion import load_transactions


# -------------------------------
# Constants
# -------------------------------

REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "amount",
    "transaction_type",
    "merchant",
    "date",
]

ALLOWED_TRANSACTION_TYPES = [
    "PAYMENT",
    "TRANSFER",
    "CASH_IN",
    "CASH_OUT",
]


# -------------------------------
# Validation functions
# -------------------------------

def validate_schema(df: pd.DataFrame) -> dict:
    """
    Validate the structure of the transaction dataset.
    """

    report = {
        "schema_valid": True,
        "missing_columns": [],
        "extra_columns": [],
        "column_types": {},
    }

    # 1. Missing columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]
    report["missing_columns"] = missing_columns

    if missing_columns:
        report["schema_valid"] = False

    # 2. Extra columns
    extra_columns = [
        column for column in df.columns
        if column not in REQUIRED_COLUMNS
    ]
    report["extra_columns"] = extra_columns

    # 3. Column dtypes
    report["column_types"] = {
        column: str(df[column].dtype)
        for column in df.columns
    }

    return report


def validate_data_types(df: pd.DataFrame) -> dict:
    """
    Validate important transaction column data types.
    """

    report = {
        "amount_numeric": False,
        "date_valid": False,
    }

    # Amount validation
    amount_check = pd.to_numeric(df["amount"], errors="coerce")
    report["amount_numeric"] = amount_check.notna().all()

    # Date validation
    date_check = pd.to_datetime(df["date"], errors="coerce")
    report["date_valid"] = date_check.notna().all()

    return report


def validate_transaction_types(df: pd.DataFrame) -> dict:
    """
    Validate transaction_type values against allowed list.
    """

    invalid_mask = ~df["transaction_type"].isin(ALLOWED_TRANSACTION_TYPES)
    invalid_count = invalid_mask.sum()

    return {
        "invalid_transaction_type_count": int(invalid_count),
        "valid": invalid_count == 0,
    }


def run_validation(df: pd.DataFrame) -> dict:
    """
    Run all validation checks.
    """

    return {
        "schema": validate_schema(df),
        "data_types": validate_data_types(df),
        "transaction_types": validate_transaction_types(df),
    }


# -------------------------------
# Analysis helpers
# -------------------------------

def analyze_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Missing value count and percentage per column.
    """

    return pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percentage": (df.isna().mean() * 100).round(2),
    })


def detect_duplicates(df: pd.DataFrame) -> dict:
    """
    Count exact duplicate rows.
    """

    duplicate_count = df.duplicated().sum()

    return {
        "duplicate_count": int(duplicate_count),
        "duplicate_percentage": round(
            duplicate_count / len(df) * 100, 2
        ) if len(df) > 0 else 0.0,
    }


# -------------------------------
# Main
# -------------------------------

if __name__ == "__main__":

    # 1. Load data
    df = load_transactions("data/raw/transactions.csv")

    # 2. Run validations
    report = run_validation(df)

    print("\n========== DATA VALIDATION ==========")

    print("\nSchema valid:",
          report["schema"]["schema_valid"])
    print("Missing columns:",
          report["schema"]["missing_columns"])
    print("Extra columns:",
          report["schema"]["extra_columns"])

    print("\nColumn types:")
    for column, dtype in report["schema"]["column_types"].items():
        print(f"  {column}: {dtype}")

    print("\nAmount numeric:",
          report["data_types"]["amount_numeric"])
    print("Date valid:",
          report["data_types"]["date_valid"])

    print("\nInvalid transaction types:",
          report["transaction_types"]["invalid_transaction_type_count"])
    print("Transaction types valid:",
          report["transaction_types"]["valid"])

    # 3. Missing values
    print("\n========== MISSING VALUES ==========")
    print(analyze_missing_values(df))

    # 4. Duplicates
    print("\n========== DUPLICATES ==========")
    print(detect_duplicates(df))