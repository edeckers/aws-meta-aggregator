from prometheus_api.utils.environment import env

APPLICATION_LOG_LEVEL = env("LOG_LEVEL", "DEBUG")

APPLICATION_LOG_RENDERER = env("LOG_RENDERER", "console")

APPLICATION_PROMETHEUS_HOST = env(
    "HOST",
    "0.0.0.0",  # nosec # B104:hardcoded_bind_all_interfaces, by design
)
APPLICATION_PROMETHEUS_PORT = int(env("PORT", "8000"))
