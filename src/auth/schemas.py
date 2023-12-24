from pydantic import BaseModel, SecretStr


# User schema in the sign-up endpoint
class User(BaseModel):
    name: str
    email: str
    password: SecretStr
