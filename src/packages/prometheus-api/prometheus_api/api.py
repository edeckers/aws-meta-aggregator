from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import prometheus_api.routers.metrics_router as mx_factory


def bootstrap_api(
    resource_label_allowlist: list[str],
    resource_tag_label_allowlist: list[str],
) -> FastAPI:
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

    metrics_router = mx_factory.create(
        resource_label_allowlist, resource_tag_label_allowlist
    )

    app.include_router(metrics_router)

    return app
