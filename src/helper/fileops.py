import concurrent.futures
import logging
from pathlib import Path

import pandas as pd
from tqdm.asyncio import tqdm

from constants.filepaths import CONTRACTS_DIR
from contract import Contract

logger = logging.getLogger(__name__)


def read_excel(file_path: Path) -> dict:
    try:
        data_dict = pd.read_excel(file_path, sheet_name=None)
        logger.debug("Excel file read successfully: %s", file_path)
        return {suite_name: suite_data.to_dict(orient="records") for suite_name, suite_data in data_dict.items()}
    except Exception as e:
        logger.error("Error reading Excel file: %s", e)
    return {}


def generate_contract_files(data: dict, suite_name: str, output_dir: Path = CONTRACTS_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)
    suite_data = data.get(suite_name, [])
    for item in suite_data:
        contract = Contract(item)
        contract.generate(output_dir=output_dir)


def load_contract_files(contract_dir: Path = CONTRACTS_DIR) -> list[Contract]:
    contracts = []
    try:
        for contract_file in contract_dir.glob("contract_*.json"):
            contract = Contract({})
            contract.load(contract_file)
            contracts.append(contract)
        logger.debug("Contract files loaded successfully from directory: %s", contract_dir)
    except Exception as e:
        logger.error("Error loading contract files: %s", e)
    return contracts


def executor(contract_dir: Path = CONTRACTS_DIR):
    # Collect all contracts
    contracts = load_contract_files(contract_dir)

    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        futures = [executor.submit(contract.verify) for contract in contracts]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Executing Contracts"):
            try:
                result = future.result()
                logger.info(f"Contract executed successfully: {result}")
            except Exception as e:
                logger.error(f"Error executing contract: {e}")
