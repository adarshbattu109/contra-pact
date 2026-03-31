import json
from pathlib import Path
import concurrent.futures
import concurrent
import requests
from tqdm import tqdm
import logging
from constants.filepaths import CONTRACTS_DIR
from helper.verify import verify_contract

logger = logging.getLogger(__name__)


def send_request(url, method="GET", data=None, headers=None):
    resp, status_code = {}, None
    try:

        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        resp = response.json()
        status_code = response.status_code
        logger.info(f"HTTP request successful: {url} with method {method}")
        logger.debug(f"Response data: {resp}")
    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request failed: {e}")
    return (status_code, resp)


def get_value_at_paths(json_data, paths) -> dict:
    results = {}
    for path in paths:
        keys = path.split(".")
        value = json_data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                value = None
                break
        results[path] = value
    logger.info(f"Extracted values for paths: {paths}")
    logger.debug(f"Extracted values: {results}")
    return results


def execute_contract_verification(base_url: str, contract_data: Path) -> dict:
    # Read the contract data from the JSON file
    with open(contract_data, "r") as f:
        contract = json.load(f)

    # ! Extract Meta from contract and send the request
    url = f"{base_url}/{contract.get('ENDPOINT', '')}"
    tc_id = contract.get("TC#")
    method = contract.get("METHOD", "GET")
    payload = contract.get("PAYLOAD", {})
    headers = contract.get("HEADERS", {})

    status_code, response_data = send_request(url=url, method=method, data=payload, headers=headers)

    logger.info(f"Executed contract: {contract_data.name} with status code: {status_code}")
    logger.debug(f"Response data for contract {contract_data.name}: {response_data}")

    # ! Perform Verification and generate Pact file
    verify_status = verify_contract(actual_response=response_data, contract=contract)
    logger.info("Verification status for contract '%s': %s", tc_id, verify_status)


def executor(base_url: str, contract_dir: Path = CONTRACTS_DIR):
    # Collect all contracts
    contracts = list(Path(contract_dir).glob("*.JSON"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        futures = [executor.submit(execute_contract_verification, base_url=base_url, contract_data=contract) for contract in contracts]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Executing Contracts"):
            try:
                result = future.result()
                logger.info(f"Contract executed successfully: {result}")
            except Exception as e:
                logger.error(f"Error executing contract: {e}")
