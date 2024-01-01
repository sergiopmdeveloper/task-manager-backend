from typing import Dict, Optional

from src.auth.exceptions import SignInWrongCredentials, UserAlreadyExists
from src.auth.schemas import AuthResponse, UserSignIn, UserSignUp
from src.auth.utils import create_access_token, get_password_hash, verify_password
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
    sign_up(user: UserSignUp) -> AuthResponse
        Sign up user
    sign_in(user: UserSignIn) -> AuthResponse
        Sign in user
    _get_user_by_email(email: str) -> Optional[Dict[str, str]]
        Get user by email
    """

    def __init__(self):
        """
        Initialize auth handler
        """

        self.client = Database().get_client()
        self.users = self.client["task-manager-db"]["users"]

    def sign_up(self, user: UserSignUp) -> AuthResponse:
        """
        Sign up user

        Parameters
        ----------
        user : UserSignUp
            User data

        Returns
        -------
        AuthResponse
            Response detail
        """

        if self._get_user_by_email(email=user.email):
            raise UserAlreadyExists()

        user_data = {
            "name": user.name,
            "email": user.email,
            "password": user.password.get_secret_value(),
        }

        user_data["password"] = get_password_hash(user_data["password"])

        self.users.insert_one(user_data)
        access_token = create_access_token()

        return AuthResponse(email=user_data["email"], access_token=access_token)

    def sign_in(self, user: UserSignIn) -> AuthResponse:
        """
        Sign in user

        Parameters
        ----------
        user : UserSignIn
            User data

        Returns
        -------
        AuthResponse
            Response detail
        """

        user_data = self._get_user_by_email(email=user.email)

        if not user_data:
            raise SignInWrongCredentials()

        if not verify_password(user.password.get_secret_value(), user_data["password"]):
            raise SignInWrongCredentials()

        access_token = create_access_token()
        email = str(user_data["email"])

        return AuthResponse(email=email, access_token=access_token)

    def _get_user_by_email(self, email: str) -> Optional[Dict[str, str]]:
        """
        Get user by email

        Parameters
        ----------
        email : str
            User email

        Returns
        -------
        Dict[str, str]
            User data
        """

        return self.users.find_one({"email": email})
