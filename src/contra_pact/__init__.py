import argparse
import logging

from constants.filepaths import CONTRACTS_DIR, PACT_DIR

logger = logging.getLogger(__name__)


def get_cli_input():
    parser = argparse.ArgumentParser(description="Contra Pact CLI")
    parser.add_argument("-t", "--test-file", type=str, help="Path to Test Excel", required=True)
    parser.add_argument("-s", "--suite", type=str, help="Suite name from the test file (sheet name)", required=True)
    parser.add_argument("-c", "--con-dir", type=str, help="Directory for saving contract files", required=False, default=CONTRACTS_DIR)
    parser.add_argument("-p", "--pact-dir", type=str, help="Directory for saving pact files", required=False, default=PACT_DIR)
    args = parser.parse_args()
    return args
