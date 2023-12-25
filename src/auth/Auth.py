from src.auth.schemas import User
from src.auth.utils import get_password_hash
from src.database.Database import Database


class Auth:
    """
    Auth handler

    Attributes
    ----------
    client : pymongo.MongoClient
        Database client
    users : pymongo.collection.Collection
        Users collection

    Methods
    -------
    sign_up(user: User) -> str
        Sign up user
    """

    def __init__(self):
        """
        Initialize auth handler
        """

        self.client = Database().get_client()
        self.users = self.client["task-manager-db"]["users"]

    def sign_up(self, user: User) -> str:
        """
        Sign up user

        Parameters
        ----------
        user : User
            User data

        Returns
        -------
        str
            User ID
        """

        user_data = {
            "name": user.name,
            "email": user.email,
            "password": user.password.get_secret_value(),
        }

        user_data["password"] = get_password_hash(user_data["password"])

        return self.users.insert_one(user_data).inserted_id
