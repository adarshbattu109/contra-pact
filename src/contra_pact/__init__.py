import logging

from constants.filepaths import CONTRACTS_DIR

logger = logging.getLogger(__name__)

import argparse


def get_cli_input():
    parser = argparse.ArgumentParser(description="Contra Pact CLI")
    parser.add_argument("-t", "--test-file", type=str, help="Path to Test Excel", required=True)
    parser.add_argument("-p", "--provider", type=str, help="Base URL for the Provider API", required=True)
    parser.add_argument("-d", "--dir", type=str, help="Directory for saving contract files", required=False, default=CONTRACTS_DIR)
    args = parser.parse_args()
    return args
