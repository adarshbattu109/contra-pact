from pathlib import Path
import pandas as pd
import logging
import json
from constants.filepaths import CONTRACTS_DIR

logger = logging.getLogger(__name__)


def read_excel(file_path: Path) -> list[dict]:
    try:
        data = pd.read_excel(file_path).to_dict(orient="records")
        logger.debug("Excel file read successfully: %s", file_path)
        return data
    except Exception as e:
        logger.error("Error reading Excel file: %s", e)
    return []


def generate_contract_files(data: list[dict], output_dir: Path = CONTRACTS_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)
    for idx, item in enumerate(data):
        file_name = item.get("TC#", f"contract_{idx+1}.json")
        save_as = Path(output_dir, file_name)
        try:
            with open(save_as, "w") as f:
                json.dump(item, f)
            logger.debug("Contract file generated successfully: %s", save_as)
        except Exception as e:
            logger.error("Error generating contract file: %s", e)
