from fastapi import APIRouter

from prometheus_api.controllers.metrics_controller import MetricsController


def create() -> APIRouter:
    router = APIRouter(
        prefix="/metrics",
        tags=["prometheus", "metrics"],
        responses={404: {"description": "Not found"}},
    )

    metrics_controller = MetricsController()

    router.add_api_route("/", metrics_controller.get_all, methods=["GET"])

    return router
