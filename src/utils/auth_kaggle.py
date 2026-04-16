import json
from kaggle.api.kaggle_api_extended import KaggleApi
import logging

logger = logging.getLogger(__name__)

class AuthKaggle:
    def __init__(self):
        self.api = KaggleApi()

    def authenticate(self):
        try:
            self.api.authenticate()
            logger.info("Successfully Authenticated!")
            return self.api
        except FileNotFoundError:
            logger.error("Credentials file not found!")
        except json.JSONDecodeError:
            logger.error("Invalid JSON!")
        except Exception as e:
            logger.error(f"Authentication error: {e}")
        return None