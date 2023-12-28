import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

from src.auth.exceptions import SecretNotProvided

load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 30


def get_password_hash(password: str) -> str:
    """
    Get password hash

    Parameters
    ----------
    password : str
        Password

    Returns
    -------
    str
        Password hash
    """

    return pwd_context.hash(password)


def create_access_token() -> str:
    """
    Create access token

    Returns
    -------
    str
        Access token

    Raises
    ------
    SecretNotProvided
        If JWT secret key is not provided
    """

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    if not JWT_SECRET_KEY:
        raise SecretNotProvided("JWT secret key not provided")

    token_props = {
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES),
    }

    return jwt.encode(claims=token_props, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
