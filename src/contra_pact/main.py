import logging
from contra_pact import get_cli_input
from helper.fileops import generate_contract_files, read_excel
from helper.helper import executor
from helper.validator import validate_data_file


logger = logging.getLogger(__name__)


def main():
    # ! Step 1: Consume CLI input
    args = get_cli_input()

    # ! Step 2: Validate the input data file
    if not validate_data_file(args.test_file):
        logger.error("Data file validation failed. Please check the logs for details.")
        return None

    # ! Step 3: Read the input data file
    contract_data = read_excel(args.test_file)

    # ! Step 4: Generate contract files from the input data file
    generate_contract_files(data=contract_data, output_dir=args.dir)
    logger.info("Contract files generated successfully in the output directory.")

    # ! Step 5: Execute the contracts and perform verification
    executor(base_url=args.provider, contract_dir=args.dir)
    logger.info("Contract execution and verification completed.")

    # ! TODO - Showcase the Summary of the results in a tabular format pretty table
