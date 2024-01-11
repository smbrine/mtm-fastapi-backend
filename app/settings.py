import os
from typing import Any

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

import ssl

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
    SERVER_BIND_HOSTNAME: str = os.getenv("SERVER_BIND_HOSTNAME", "127.0.0.1")
    SERVER_BIND_PORT: int = os.getenv("SERVER_BIND_PORT", 8000)
    SSL_CERT_PATH: str = os.getenv("SSL_CERT_PATH", "./ssl/cert.pem")
    SSL_KEY_PATH: str = os.getenv("SSL_KEY_PATH", "./ssl/key.pem")
    IS_HTTPS: bool = os.getenv("IS_HTTPS", 0)


settings = Settings()
