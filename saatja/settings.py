from typing import Set, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_KEYS: Set[str] = {"mellon"}  # Valid X-API-Key values
    WEBHOOK_PREFIXES: Set[str] = {"https://"}  # Allowed URL prefixes for webhooks
    DB_COLLECTION_PREFIX: str = ""  # In case sharing a Google Cloud Firestore project
    PORT: int = 8080  # According to Google Cloud Run container contract
    GCLOUD_PROJECT: Optional[str]  # If set configures logging for GCloud compatibility


conf = Settings()
# Ensure "if WEBHOOK_PREFIXES" does not pass with empty string
if conf.WEBHOOK_PREFIXES == {""}:
    conf.WEBHOOK_PREFIXES = set()
