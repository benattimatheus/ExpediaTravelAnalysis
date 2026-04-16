import logging

logger = logging.getLogger(__name__)

def read_and_insert_data_from_csv(conn, file_path):
    cur = conn.cursor()
    logger.info(f"[INGESTION] Starting load: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            cur.copy_expert(
                """
                COPY expedia_raw
                FROM STDIN
                WITH CSV HEADER
                """,
                f
            )

        conn.commit()
        logger.info(f"[INGESTION] Successfully loaded: {file_path}")

    except Exception:
        logger.exception(f"[INGESTION] Failed loading: {file_path}")
        conn.rollback()
        raise

    finally:
        cur.close()