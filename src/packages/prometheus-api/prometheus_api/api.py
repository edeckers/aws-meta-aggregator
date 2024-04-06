from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import prometheus_api.routers.metrics_router as mx_factory


def bootstrap_api() -> FastAPI:
    app = FastAPI()

    origins = ["*"]

    # FIXME ED Get rid of this
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    metrics_router = mx_factory.create()

    app.include_router(metrics_router)

    return app
