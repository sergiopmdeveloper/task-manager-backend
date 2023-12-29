from unittest.mock import MagicMock, patch

import pytest
from pytest import MonkeyPatch

from src.database.Database import Database
from src.database.exceptions import (
    ConnectionStringException,
    DatabaseConnectionException,
    DatabaseResponseException,
)


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


def test_database_connection_string_error(
    database: Database, monkeypatch: MonkeyPatch
) -> None:
    """
    Test if the connection string is not provided

    Parameters
    ----------
    database : Database
        Database instance
    monkeypatch : MonkeyPatch
        A pytest fixture for monkeypatching items
    """

    monkeypatch.delenv("MONGODB_CONNECTION_STRING")

    with pytest.raises(ConnectionStringException) as exception:
        database.get_client()

    assert str(exception.value) == "Connection string not provided"


def test_database_connection_string_is_injected(database: Database) -> None:
    """
    Test if the connection string is injected

    Parameters
    ----------
    database : Database
        Database instance
    """

    database._set_connection_string()

    assert database._Database__connection_string == "fake_connection_string"


def test_database_client_error(database: Database) -> None:
    """
    Test if there is an error connecting to the database

    Parameters
    ----------
    database : Database
        Database instance
    """

    with patch("src.database.Database.MongoClient") as mock_client:
        mock_client.side_effect = Exception

        with pytest.raises(DatabaseConnectionException) as exception:
            database.get_client()

        assert str(exception.value) == "Error connecting to database"


def test_database_response_error(database: Database) -> None:
    """
    Test if there is an error in the response from the database

    Parameters
    ----------
    database : Database
        Database instance
    """

    with patch("src.database.Database.MongoClient") as mock_client:
        mock_client.admin.command.side_effect = Exception

        with pytest.raises(DatabaseResponseException) as exception:
            database._test_connection(client=mock_client)

        assert str(exception.value) == "Error in database response"


def test_database_get_client_returns_client(database: Database) -> None:
    """
    Test if the client is returned in get_client

    Parameters
    ----------
    database : Database
        Database instance
    """

    with patch("src.database.Database.MongoClient") as mock_client:
        mock_client.return_value = MagicMock()
        client = database.get_client()

    assert client == mock_client.return_value


def test_database_get_client_methods_are_called(database: Database) -> None:
    """
    Test if the methods of get_client are called

    Parameters
    ----------
    database : Database
        Database instance
    """

    with (
        patch("src.database.Database.MongoClient") as mock_client,
        patch(
            "src.database.Database.Database._set_connection_string"
        ) as mock_set_connection_string,
        patch(
            "src.database.Database.Database._test_connection"
        ) as mock_test_connection,
    ):
        database.get_client()

    mock_client.assert_called_once()
    mock_set_connection_string.assert_called_once()
    mock_test_connection.assert_called_once()
