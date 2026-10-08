import pandas as pd
import numpy as np
from pathlib import Path


def generate_transactions(n=1000):

    np.random.seed(42)

    transaction_types = [
        "PAYMENT",
        "TRANSFER",
        "CASH_IN",
        "CASH_OUT"
    ]

    merchants = [
        "Amazon",
        "Netflix",
        "Daraz",
        "Foodpanda",
        "Alfalah Bank",
        "HBL",
        "Meezan Bank"
    ]

    df = pd.DataFrame({
        "transaction_id": [
            f"TX{i:06d}" for i in range(1, n + 1)
        ],

        "customer_id": [
            f"C{i:05d}" for i in np.random.randint(1, 300, n)
        ],

        "amount": np.random.lognormal(
            mean=7,
            sigma=1,
            size=n
        ).round(2),

        "transaction_type": np.random.choice(
            transaction_types,
            size=n
        ),

        "merchant": np.random.choice(
            merchants,
            size=n
        ),

        "date": pd.date_range(
            start="2026-01-01",
            periods=n,
            freq="h"
        )
    })

    # -----------------------------
    # Introduce data quality issues
    # -----------------------------

    # Missing customer IDs
    df.loc[10:19, "customer_id"] = np.nan

    # Missing amounts
    df.loc[20:24, "amount"] = np.nan

    # Negative amounts
    df.loc[30:34, "amount"] = -500

    # Zero amounts
    df.loc[40:44, "amount"] = 0

    # Invalid transaction types
    df.loc[50:54, "transaction_type"] = "INVALID"

    # Missing merchants
    df.loc[60:69, "merchant"] = np.nan

    # Extreme outliers
    df.loc[70:74, "amount"] = 10_000_000

    # Duplicate rows
    duplicates = df.iloc[100:110].copy()
    df = pd.concat([df, duplicates], ignore_index=True)

    # Save
    output_path = Path("data/raw/transactions.csv")

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(f"Dataset created: {output_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")


if __name__ == "__main__":
    generate_transactions()