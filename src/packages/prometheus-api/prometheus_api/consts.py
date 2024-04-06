from prometheus_api.utils.environment import env

APPLICATION_LOG_LEVEL = env("LOG_LEVEL", "DEBUG")

APPLICATION_LOG_RENDERER = env("LOG_RENDERER", "console")
