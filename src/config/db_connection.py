import psycopg2
import os
from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)

def get_connection():
    load_dotenv()
    logger.info("Starting connection to database.")

    try:
        conn = psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        logger.info("Successfully connected to database.")
        return conn

    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

def run_sql_file(conn, path):
    cur = conn.cursor()
    logger.info(f"Running SQL file: {path}")

    try:
        with open(path, "r") as f:
            sql = f.read()

        cur.execute(sql)
        conn.commit()

        logger.info(f"Successfully executed: {path}")

    except Exception as e:
        logger.error(f"Failed to execute {path}: {e}")
        conn.rollback()
        raise

    finally:
        cur.close()