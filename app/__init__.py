from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.settings import settings
from db.database import sessionmanager
