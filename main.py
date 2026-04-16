import os
from dotenv import load_dotenv

from src.ingestion.download_file import run_kaggle_download
from src.config.db_connection import get_connection
from src.utils.logger import setup_logger
from src.pipeline.data_pipeline import DataPipeline

base_dir = os.path.dirname(os.path.abspath(__file__))

dataset_name = "jacopoferretti/expedia-travel-dataset"
expected_file = "travel.csv"


def main():
    load_dotenv()
    setup_logger()

    run_kaggle_download(base_dir, dataset_name, expected_file)

    conn = get_connection()

    try:
        pipeline = DataPipeline(conn)
        pipeline.run_all()
    finally:
        conn.close()


if __name__ == "__main__":
    main()