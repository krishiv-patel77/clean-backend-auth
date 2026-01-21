"""
FASTAPI ROOT FILE 
"""

from fastapi import FastAPI
from src.logging import configure_logging, LogLevels
from src.auth.router import router as auth_router
from src.users.router import router as users_router

configure_logging(LogLevels.info)

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)