import logging
import os

def setup_logger():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, "logs")

    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "logs.txt")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("ExpediaAnalysis")

logger = setup_logger()