import os

APPLICATION_PREFIX = "PROMETHEUS_API_"


def env(name: str, default: str) -> str:
    return os.getenv(f"{APPLICATION_PREFIX}{name}", default)
