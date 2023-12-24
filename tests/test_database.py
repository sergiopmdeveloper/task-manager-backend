from unittest.mock import patch

import pytest

from src.database.Database import Database
from src.database.exceptions import (
    DatabaseConnectionException,
    DatabaseResponseException,
)


@pytest.fixture
def database() -> Database:
    """
    Returns a Database instance

    Returns
    -------
    Database
        Database instance
    """

    return Database()


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
