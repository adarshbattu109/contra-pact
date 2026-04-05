"""Class to represent a contract"""

import json
import logging
import re
from pathlib import Path

from constants.filepaths import CONTRACTS_DIR, PACT_DIR
from helper.helper import get_value_at_paths, send_request

logger = logging.getLogger(__name__)


class Contract:
    """Class to represent a contract"""

    def __init__(self, data: dict):

        self.id: str = data.get("id", "")
        self.suite: str = data.get("suite", "")
        self.url: str = data.get("url", "")
        self.headers: dict = data.get("headers", {})
        self.payload: dict = data.get("payload", {})
        self.timeout: int = data.get("timeout", 10)
        self.method: str = data.get("request_type", "GET")
        self.query_params: dict = data.get("query_params", {})

        # ! Add all keys starting with '$' in the data as verifications. They represent JSON Paths and their expected regex patterns.s
        self.verifications: list = [{"path": key, "regex": value} for key, value in data.items() if key.startswith("$")]
        self.verifications.append({"status_code": "status_code", "regex": data.get("status_code", 200)})

    def generate(self, output_dir: Path = CONTRACTS_DIR):
        output_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"contract_{self.suite}_{self.id}.json"
        save_as = Path(output_dir, file_name)
        try:
            with open(save_as, "w") as f:
                json.dump(obj=self.__dict__, fp=f, ensure_ascii=False, indent=4)
            logger.debug("Contract file generated successfully: %s", save_as)
        except Exception as e:
            logger.error("Error generating contract file: %s", e)

    def load(self, contract_file: Path):
        try:
            with open(contract_file, "r") as f:
                data = json.load(f)
            self.__init__(data)
            logger.debug("Contract file loaded successfully: %s", contract_file)
        except Exception as e:
            logger.error("Error loading contract file: %s", e)

    def _pact(self, output_dir: Path = PACT_DIR):
        output_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"pact_{self.suite}_{self.id}.json"
        save_as = Path(output_dir, file_name)
        try:
            with open(save_as, "w") as f:
                json.dump(obj=self.__dict__, fp=f, ensure_ascii=False, indent=4)
            logger.debug("Pact file generated successfully: %s", save_as)
        except Exception as e:
            logger.error("Error generating pact file: %s", e)

    def verify(self):
        resp, status_code = send_request(url=self.url, method=self.method, data=self.payload, headers=self.headers)

        updated_verifications = []
        for verification in self.verifications:
            if "status_code" in verification:
                expected_status = verification["regex"]
                matches = re.findall(string=str(status_code), pattern=expected_status, flags=re.DOTALL)

                logger.info(f"Status code verification passed: {status_code}") if matches else logger.error(f"Status code verification failed: expected {expected_status}, got {status_code}")

                updated_verifications.append({"status_code": "status_code", "regex": verification["regex"], "value": status_code, "status": "PASS" if matches else "FAIL"})
            else:
                path, regex = verification["path"], verification["regex"]
                value = get_value_at_paths(resp, [path]).get(path)
                matches = re.findall(string=str(value), pattern=regex, flags=re.DOTALL)
                (
                    logger.error(f"Regex verification failed for path '{path}': expected pattern '{regex}', got '{value}'")
                    if not matches
                    else logger.info(f"Regex verification passed for path '{path}': value '{value}' matches pattern '{regex}'")
                )
                updated_verifications.append({"path": path, "regex": regex, "value": value, "status": "PASS" if matches else "FAIL"})
        self.verifications = updated_verifications

        # Generate pact file with verification results
        self._pact()
