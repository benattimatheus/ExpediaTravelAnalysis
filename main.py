import os
from src.ingestion.download_file import run_kaggle_download
from src.config.db_connection import get_connection
from src.config.db_connection import run_sql_file
from src.utils.logger import setup_logger

base_dir = os.path.dirname(os.path.abspath(__file__))

dataset_name = "jacopoferretti/expedia-travel-dataset"
expected_file = "travel.csv"

def main():
    run_kaggle_download(base_dir, dataset_name, expected_file)
    conn = get_connection()
    setup_logger()

    try:
        run_sql_file(conn, "sql/bronze/create_expedia_raw.sql")
        #run_sql_file(conn, "sql/silver/create_expedia_clean.sql")
        #run_sql_file(conn, "sql/gold/create_fact_user_behavior.sql")
    finally:
        conn.close()

if __name__ == "__main__":
    main()