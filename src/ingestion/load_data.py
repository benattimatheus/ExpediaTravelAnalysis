import logging

logger = logging.getLogger(__name__)

def read_and_insert_data_from_csv(conn, file_path):
    cur = conn.cursor()
    logger.info(f"[INGESTION] Starting load: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            cur.copy_expert(
                """
                COPY expedia_raw (
                    id,
                    date_time,
                    site_name,
                    posa_continent,
                    user_location_country,
                    user_location_region,
                    user_location_city,
                    orig_destination_distance,
                    user_id,
                    is_mobile,
                    is_package,
                    channel,
                    srch_ci,
                    srch_co,
                    srch_adults_cnt,
                    srch_children_cnt,
                    srch_rm_cnt,
                    srch_destination_id,
                    srch_destination_type_id,
                    is_booking,
                    cnt,
                    hotel_continent,
                    hotel_country,
                    hotel_market,
                    hotel_cluster
                )
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