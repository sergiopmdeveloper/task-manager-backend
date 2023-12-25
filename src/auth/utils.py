from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password) -> str:
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
