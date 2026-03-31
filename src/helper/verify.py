import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


def generate_pact(contract_data: dict, results: dict) -> Path: ...


def verify_value(actual, expected_regex):
    matches = re.findall(string=actual, pattern=rf"{expected_regex}", flags=re.DOTALL)
    logger.info("Matches found in value: %s as '%s'", actual, matches)
    if matches:
        logger.info("Verification successful: Values match.")
    else:
        logger.warning("Verification failed: No matches found.")
    return bool(matches)


def verify_contract(actual_response: dict, contract: dict) -> bool:
    results = []
    expected_response = contract.get("EXPECTED_RESPONSE", {})
    for key, expected_value in expected_response.items():
        status = True
        actual_value = actual_response.get(key)
        if not verify_value(str(actual_value), str(expected_value)):
            logger.warning("Contract verification failed for key: %s", key)
            status = False
        else:
            logger.info("Contract verification successful for key: %s", key)
        results.append({"expected": expected_value, "actual": actual_response.get(key), "status": status})
    overall_verification_status = all([result["status"] for result in results])
    logger.info("Overall contract verification status: %s", overall_verification_status)
    results.append({"TC#": contract.get("TC#"), "status": overall_verification_status})

    # TODO - Generate the Pact File using contract data and the results
    # generate_pact
    return overall_verification_status
