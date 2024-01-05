from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.auth.router import auth_router

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
