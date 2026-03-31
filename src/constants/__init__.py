import logging
from pathlib import Path
from datetime import datetime

from constants.filepaths import LOG_DIR


prefix = "contra_pact"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"{prefix}_{timestamp}.log"
log_file = Path(LOG_DIR, log_filename)

log_file.parent.mkdir(parents=True, exist_ok=True)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=log_file,
)


logger = logging.getLogger(__name__)
