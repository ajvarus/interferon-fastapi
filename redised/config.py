# /redised.config.py

import os

REDIS_HOST: str = os.environ.get("REDIS_HOST")
REDIS_PORT: int = int(os.environ.get("REDIS_PORT"))
REDIS_DB: int = int(os.environ.get("REDIS_DB"))