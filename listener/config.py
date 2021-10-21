"""Global constants across the application"""

from typing import Optional

from pydantic import BaseSettings, Field


# APP CONSTANTS
# ================================================================
class Settings(BaseSettings):
    jarvis_host: str = "localhost"
    jarvis_port: int = 7411

    class Config:
        env_file = ".env"


settings = Settings()
