from src.config.db_connection import run_sql_file
from src.ingestion.load_data import read_and_insert_data_from_csv

class DataPipeline:
    def __init__(self, conn):
        self.conn = conn

    def run_bronze(self):
        run_sql_file(self.conn, "sql/bronze/create_expedia_raw.sql")

    # def run_silver(self):
    #    run_sql_file(self.conn, "sql/silver/create_expedia_clean.sql")
    #
    # def run_gold(self):
    #    run_sql_file(self.conn, "sql/gold/create_fact_user_behavior.sql")

    def run_ingestion(self):
        read_and_insert_data_from_csv(self.conn, "data/raw/travel.csv")

    def run_all(self):
        self.run_bronze()
        #    self.run_silver()
        #    self.run_gold()
        self.run_ingestion()
