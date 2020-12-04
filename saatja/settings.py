from typing import Set

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_KEYS: Set[str] = {"mellon"}  # Valid X-API-Key values
    WEBHOOK_PREFIXES: Set[str] = {"https://"}  # Allowed URL prefixes for webhooks
    DB_COLLECTION_PREFIX: str = ""  # In case sharing a Google Cloud Firestore project
    PORT: int = 8080  # According to Google Cloud Run container contract


conf = Settings()
