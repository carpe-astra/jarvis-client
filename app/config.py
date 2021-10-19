"""Global constants across the application"""

import pathlib
from typing import Optional

from pydantic import BaseSettings, Field

# APP CONSTANTS
# ================================================================
APP_DIR = pathlib.Path(__file__).parent
APP_DIR_NAME = "app"
MODULES_DIR_NAME = "modules"
MODULES_DIR = APP_DIR / MODULES_DIR_NAME

DEV = "development"
TEST = "test"
PROD = "production"


class Settings(BaseSettings):
    app_name: str = "Jarvis Client"
    app_description: str = "A helpful AI voice assistant"
    app_version: str = "0.1.0"

    API_V1_STR: str = "/api/v1"

    fastapi_env: str = PROD

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379

    class Config:
        env_file = ".env"


settings = Settings()
