import csv
import logging

logger = logging.getLogger(__name__)

def validate_csv_schema(file_path, expected_columns):
    logger.info(f"Validating CSV schema: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)

        logger.debug(f"Detected header: {header}")

        if header != expected_columns:
            logger.error(
                f"Schema mismatch. Expected: {expected_columns}, Got: {header}"
            )
            raise ValueError(
                f"Invalid schema. Expected: {expected_columns}, Got: {header}"
            )

        logger.info("CSV schema validation passed successfully.")

    except Exception as e:
        logger.exception(f"Failed to validate CSV schema: {file_path}")
        raise