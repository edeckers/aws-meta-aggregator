from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from aws_meta_aggregator.responses.paginator import Paginator


@dataclass(frozen=True)
class Cost:  # pylint: disable=too-many-instance-attributes
    dimension: str
    name: str
    cost: float
    currency: str


class Costs:  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        # client: CostGroupsTaggingAPIClient
        client: Any,
    ) -> None:
        self.__client = client

    def __retrieve_for_resources_batch(
        self, time_start: datetime, time_end: datetime, dimension: str
    ) -> list[Cost]:
        resources_metas: list[Cost] = []

        time_end = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        time_start = time_end - timedelta(days=5)

        paginator = Paginator(
            lambda token: self.__client.get_cost_and_usage(
                Granularity="HOURLY",
                Metrics=[
                    "AmortizedCost",
                ],
                **({"NextPageToken": token} if token else {}),
                TimePeriod={
                    "Start": time_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "End": time_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
                GroupBy=[
                    {"Type": "DIMENSION", "Key": dimension},
                ],
            ),
            "NextPageToken",
        )

        for page in paginator.page():
            time_periods = page["ResultsByTime"]

            for time_period in time_periods:
                for group in time_period["Groups"]:
                    resources_metas.append(
                        Cost(
                            dimension=dimension,
                            name=group["Keys"][0],
                            cost=float(group["Metrics"]["AmortizedCost"]["Amount"]),
                            currency="USD",
                        )
                    )

        return resources_metas

    def retrieve_for_resources(self) -> list[Cost]:
        resources_metas: list[Cost] = []

        time_end = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        time_start = time_end - timedelta(days=5)

        for dimension in ["SERVICE", "INSTANCE_TYPE", "REGION"]:
            resources_metas.extend(
                self.__retrieve_for_resources_batch(
                    time_start=time_start,
                    time_end=time_end,
                    dimension=dimension,
                )
            )

        return resources_metas
