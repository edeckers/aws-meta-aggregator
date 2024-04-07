from fastapi import APIRouter

from prometheus_api.controllers.metrics_controller import MetricsController


def create(
    resource_label_allowlist: list[str],
    resource_tag_label_allowlist: list[str],
) -> APIRouter:
    router = APIRouter(
        prefix="/metrics",
        tags=["prometheus", "metrics"],
        responses={404: {"description": "Not found"}},
    )

    metrics_controller = MetricsController(
        resource_label_allowlist=resource_label_allowlist,
        resource_tag_label_allowlist=resource_tag_label_allowlist,
    )

    router.add_api_route("/", metrics_controller.get_all, methods=["GET"])

    return router
