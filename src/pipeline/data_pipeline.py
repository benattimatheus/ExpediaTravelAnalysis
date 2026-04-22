from src.config.db_connection import run_sql_file
from src.ingestion.load_data import read_and_insert_data_from_csv
from src.modeling.train import run_model_training


class DataPipeline:
    def __init__(self, conn, engine):
        self.conn = conn
        self.engine = engine

    def run_bronze(self):
        run_sql_file(self.conn, "sql/bronze/create_expedia_raw.sql")

    def run_truncate(self):
        run_sql_file(self.conn, "sql/bronze/truncate_expedia_raw.sql")

    def run_silver(self):
        run_sql_file(self.conn, "sql/silver/create_expedia_silver.sql")

    def run_gold(self):
        run_sql_file(self.conn, "sql/gold/conversion.sql")
        run_sql_file(self.conn, "sql/gold/booking_window.sql")
        run_sql_file(self.conn, "sql/gold/destination.sql")
        run_sql_file(self.conn, "sql/gold/distance.sql")
        run_sql_file(self.conn, "sql/gold/hotel_cluster_performance.sql")
        run_sql_file(self.conn, "sql/gold/user_behavior.sql")
        run_sql_file(self.conn, "sql/gold/model_dataset.sql")

    def run_ingestion(self):
        read_and_insert_data_from_csv(self.conn, "data/raw/travel.csv")

    def run_modeling(self):
        return run_model_training(self.engine)

    def run_all(self):
        self.run_bronze()
        self.run_truncate()
        self.run_ingestion()
        self.run_silver()
        self.run_gold()
        return self.run_modeling()