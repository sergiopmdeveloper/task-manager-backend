class ConnectionStringException(Exception):
    """
    Exception that is raised when
    the connection string is not provided
    """

    pass


class DatabaseConnectionException(Exception):
    """
    Exception that is raised when
    the database connection fails
    """

    pass


class DatabaseResponseException(Exception):
    """
    Exception that is raised when
    database does not respond correctly
    """

    pass
