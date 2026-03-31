from pathlib import Path
import logging
import pandas as pd

from constants.constants import MANDATORY_CONTRACT_COLUMNS

logger = logging.getLogger(__name__)


def check_file_exists(file_path: Path) -> bool:
    if file_path.exists():
        logger.info("File exists: %s", file_path)
    else:
        logger.warning("File does not exist: %s", file_path)
    return file_path.exists()


def check_file_format(file_path: Path, expected_format: str = ".xlsx") -> bool:
    status = file_path.suffix == expected_format
    if status:
        logger.info("File format is correct: %s", file_path)
    else:
        logger.warning("File format is incorrect: %s", file_path)
    return status


def check_mandatory_columns(file_path: Path, mandatory_columns: list[str]) -> bool:
    try:
        df = pd.read_excel(file_path)
        missing_columns = [col for col in mandatory_columns if col not in df.columns]
        status = not missing_columns
        if status:
            logger.info("All mandatory columns are present in the file: %s", file_path)
        else:
            logger.warning("Missing mandatory columns in the file %s: %s", file_path, missing_columns)
    except Exception as e:
        logger.error("Error reading Excel file for column validation: %s", e)
        return False
    return status


def validate_data_file(file_path: Path) -> bool:
    return all(
        [
            check_file_exists(file_path),
            check_file_format(file_path),
            check_mandatory_columns(file_path, mandatory_columns=MANDATORY_CONTRACT_COLUMNS),
        ]
    )
