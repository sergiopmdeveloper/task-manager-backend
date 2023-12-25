import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
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
    """

    token_props = {
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES),
    }

    return jwt.encode(claims=token_props, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
