from src.ingestion import load_transactions

from src.validation import (
    validate_schema,
    validate_data_types,
    validate_transaction_types,
    analyze_missing_values,
    detect_duplicates
)

from src.cleaning import (
    detect_invalid_amounts,
    clean_basic_values
)

from src.logger import get_logger

logger = get_logger()

from src.outliers import (
    detect_outliers_iqr
)

from src.reporting import (
    save_quality_report
)


RAW_FILE = "data/raw/transactions.csv"

CLEAN_FILE = (
    "data/processed/clean_transactions.csv"
)

REPORT_FILE = (
    "data/reports/quality_report.json"
)


def run_pipeline():

    logger.info("\n==============================")
    logger.info("FINTECH DATA QUALITY ENGINE")
    logger.info("==============================")

    # 1. INGESTION
    logger.info("\n[1] Loading data...")

    df = load_transactions(RAW_FILE)

    logger.info(
        f"Loaded {len(df)} rows"
    )

    # 2. VALIDATION
    logger.info("\n[2] Validating data...")

    schema = validate_schema(df)

    types = validate_data_types(df)

    transaction_types = (
        validate_transaction_types(df)
    )

    # 3. QUALITY ANALYSIS
    logger.info("\n[3] Analyzing quality...")

    missing = analyze_missing_values(df)

    duplicates = detect_duplicates(df)

    invalid_amounts = (
        detect_invalid_amounts(df)
    )

    outliers = detect_outliers_iqr(df)

    # 4. CLEANING
    logger.info("\n[4] Cleaning data...")

    clean_df = clean_basic_values(df)

    # Save clean data
    clean_df.to_csv(
        CLEAN_FILE,
        index=False
    )

    # 5. REPORT
    logger.info("\n[5] Creating report...")

    report = {
        "dataset": {
            "original_rows": len(df),
            "clean_rows": len(clean_df),
            "removed_rows": (
                len(df) - len(clean_df)
            )
        },

        "schema": schema,

        "data_types": types,

        "transaction_types": transaction_types,

        "missing_values": (
            missing.to_dict()
        ),

        "duplicates": duplicates,

        "invalid_amounts": invalid_amounts,

        "outliers": outliers
    }

    save_quality_report(
        report,
        REPORT_FILE
    )

    logger.info("\n==============================")
    logger.info("PIPELINE COMPLETED")
    logger.info("\n==============================")

    logger.info(
        f"\nClean dataset: {CLEAN_FILE}"
    )

    logger.info(
        f"Quality report: {REPORT_FILE}"
    )


if __name__ == "__main__":
    run_pipeline()