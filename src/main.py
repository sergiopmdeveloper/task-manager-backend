from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.auth.router import auth_router

app = FastAPI()

app.include_router(auth_router)


@app.get("/")
def root() -> RedirectResponse:
    """
    Redirects to the docs page

    Returns
    -------
    RedirectResponse
        Redirects to the docs page
    """

    return RedirectResponse(url="/docs")
