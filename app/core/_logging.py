import sys

from loguru import logger

from app import config

LOG_DIR = config.APP_DIR.parent / "logs"

if config.settings.fastapi_env == config.PROD:
    logger.add(
        LOG_DIR / "app.jsonl",
        rotation="500 MB",
        retention="10 days",
        serialize=True,
        level="INFO",
    )
elif config.settings.fastapi_env == config.TEST:
    logger.add(
        LOG_DIR / "app.jsonl",
        rotation="500 MB",
        retention="10 days",
        serialize=True,
        level="INFO",
    )
elif config.settings.fastapi_env == config.DEV:
    logger.add(sys.stderr, level="DEBUG")
else:
    raise ValueError(f"Unknown FASTAPI_ENV: {config.settings.fastapi_env}")

logger.info("Deploying application with settings", config=config.settings)
