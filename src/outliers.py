import pandas as pd


def detect_outliers_iqr(
    df,
    column="amount"
):

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    mask = (
        (df[column] < lower) |
        (df[column] > upper)
    )

    return {
        "lower_bound": round(lower, 2),
        "upper_bound": round(upper, 2),
        "outlier_count": int(mask.sum()),
        "outlier_percentage": round(
            mask.mean() * 100,
            2
        )
    }


from src.outliers import detect_outliers_iqr
from src.ingestion import load_transactions

df = load_transactions("data/raw/transactions.csv")

result = detect_outliers_iqr(df)

print(result)