from fastapi import APIRouter

from src.auth.schemas import User

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/sign-up")
def sign_up(user: User) -> User:
    ...

    return user
