import logging

import requests

logger = logging.getLogger(__name__)


def send_request(url, method="GET", data=None, headers=None) -> tuple[int, dict]:
    status_code, resp = 400, {}
    try:

        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=data)
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
