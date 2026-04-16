import os
import sys
from src.utils.auth_kaggle import AuthKaggle
from src.utils.downloader_kaggle import KaggleRepository
from src.utils.logger import logger


def run_kaggle_download(base_dir, dataset_name, expected_file):

    credentials_path = os.path.join(base_dir, ".kaggle", "kaggle.json")
    download_path = os.path.join(base_dir, "data", "raw")
    dataset_path = os.path.join(download_path, expected_file)

    logger.info("Starting Kaggle authentication.")

    auth = AuthKaggle()
    api = auth.authenticate()

    if not api:
        logger.error("Kaggle authentication failed.")
        sys.exit(1)

    logger.info("Authentication successful. Downloading dataset.")

    os.makedirs(download_path, exist_ok=True)

    repo = KaggleRepository(api)
    repo.download_dataset(dataset_name, download_path)

    if not os.listdir(download_path):
        logger.error("Download failed: empty directory.")
        sys.exit(1)

    logger.info("Download completed successfully.")