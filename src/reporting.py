import json
from pathlib import Path


def save_quality_report(report, output_path):

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            default=str
        )

    print(
        f"Report saved: {output_path}"
    )




def calculate_quality_score(
    df,
    missing_count,
    duplicate_count,
    invalid_count,
    outlier_count
):

    total_cells = df.shape[0] * df.shape[1]

    missing_penalty = (
        missing_count / total_cells * 100
    )

    duplicate_penalty = (
        duplicate_count / len(df) * 100
    )

    invalid_penalty = (
        invalid_count / len(df) * 100
    )

    outlier_penalty = (
        outlier_count / len(df) * 100
    )

    score = 100 - (
        missing_penalty
        + duplicate_penalty
        + invalid_penalty
        + outlier_penalty
    )

    return round(
        max(score, 0),
        2
    )