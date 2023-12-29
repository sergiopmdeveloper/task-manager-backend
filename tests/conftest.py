import pytest
from pytest import MonkeyPatch

from src.database.Database import Database


@pytest.fixture
def database(monkeypatch: MonkeyPatch) -> Database:
    """
    Returns a Database instance

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        A pytest fixture for monkeypatching items

    Returns
    -------
    Database
        Database instance
    """

    monkeypatch.setenv("MONGODB_CONNECTION_STRING", "fake_connection_string")

    return Database()
