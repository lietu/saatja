from os import environ

import google.auth.credentials
from firedantic.configurations import configure
from google.cloud import firestore

from saatja.settings import conf


def _make_test_credentials():
    from mock import Mock

    return Mock(spec=google.auth.credentials.Credentials)


def get_db() -> firestore.Client:
    """Returns the database client.

    :return: Firestore client.
    """
    if environ.get("FIRESTORE_EMULATOR_HOST"):
        return firestore.Client(
            project="saatja",
            credentials=_make_test_credentials(),
        )
    else:
        # Autodetect in Google Cloud Run works pretty well
        return firestore.Client()


def get_prefix() -> str:
    """Returns the prefix for the database collection.

    :return: The prefix.
    """
    prefix = ""
    if conf.DB_COLLECTION_PREFIX:
        prefix += f"{conf.DB_COLLECTION_PREFIX}-"

    return prefix


def configure_mock_db() -> None:
    from mockfirestore import MockFirestore

    mock_db = MockFirestore()
    configure(mock_db, "")


def configure_db() -> None:
    configure(get_db(), get_prefix())
