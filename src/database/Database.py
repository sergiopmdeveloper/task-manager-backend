import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.database.exceptions import (
    DatabaseConnectionException,
    DatabaseResponseException,
)

"""
Load environment variables
"""

load_dotenv()


class Database:
    """
    Database handler

    Attributes
    ----------
    __connection_string : str
        Connection string to connect to database

    Methods
    -------
    get_client()
        Connect to database and set client
    _test_connection(client)
        Test connection to database
    """

    def __init__(self) -> None:
        """
        Initialize database handler
        """

        self.__connection_string = os.environ["MONGODB_CONNECTION_STRING"]

    def get_client(self) -> MongoClient:
        """
        Connect to database and set client

        Raises
        ------
        DatabaseConnectionException
            If there is an error connecting to the database
        """

        try:
            client = MongoClient(self.__connection_string, server_api=ServerApi("1"))
        except:
            raise DatabaseConnectionException("Error connecting to database")

        self._test_connection(client=client)

        return client

    def _test_connection(self, client: MongoClient) -> None:
        """
        Test connection to database

        Parameters
        ----------
        client : MongoClient
            Database client

        Raises
        ------
        DatabaseResponseException
            If there is an error in the database response
        """

        try:
            client.admin.command("ping")
        except:
            raise DatabaseResponseException("Error in database response")
