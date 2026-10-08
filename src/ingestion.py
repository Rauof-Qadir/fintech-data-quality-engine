from pathlib import Path
import pandas as pd


def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Load raw transaction data from CSV.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    if path.suffix.lower() != ".csv":
        raise ValueError(
            "Only CSV files are currently supported."
        )

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError(
            "The transaction file is empty."
        )

    return df


if __name__ == "__main__":

    file_path = "data/raw/transactions.csv"

    df = load_transactions(file_path)

    print("Data loaded successfully!")
    print()
    print("Shape:", df.shape)
    print()
    print(df.head())