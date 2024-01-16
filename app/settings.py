import os
import pathlib
from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
    SERVER_BIND_HOSTNAME: str = os.getenv("SERVER_BIND_HOSTNAME", "127.0.0.1")
    SERVER_BIND_PORT: int = int(os.getenv("SERVER_BIND_PORT", 8000))

    SSL_CERT_PATH: str = os.getenv("SSL_CERT_PATH", "./ssl/cert.pem")
    SSL_KEY_PATH: str = os.getenv("SSL_KEY_PATH", "./ssl/key.pem")
    IS_HTTPS: bool = bool(int(os.getenv("IS_HTTPS", 0)))

    @field_validator("SSL_CERT_PATH", "SSL_KEY_PATH")
    @classmethod
    def provide_with_abspath(cls, v: str) -> str:
        if pathlib.Path(v).is_absolute():
            return v
        return str(pathlib.Path(__file__).parents[1]) + v.replace("./", "/")


settings = Settings()
