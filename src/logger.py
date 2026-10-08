import logging
from pathlib import Path


def get_logger(name="fintech_quality_engine"):

    log_dir = Path("data/logs")
    log_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )

    file_handler = logging.FileHandler(
        log_dir / "pipeline.log"
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger