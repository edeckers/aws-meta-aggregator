from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _sanitize_resource_info(resource_info_parts: list[str]) -> tuple[str | None, str]:
    if len(resource_info_parts) == 1:
        parts = resource_info_parts[0].split("/")

        if len(parts) == 1:
            return None, parts[0]

        return parts[0], parts[1]

    if len(resource_info_parts) == 2:
        return resource_info_parts[0], resource_info_parts[1]

    raise ValueError("Invalid ARN")


def _parse_arn(arn: str) -> tuple[str, str, str, str, str | None, str]:
    parts = arn.removeprefix("arn:").split(":")

    if not (5 <= len(parts) <= 6):
        raise ValueError("Invalid ARN")

    partition, service, region, account, *resource_info = parts

    maybe_resource_type, resource_id = _sanitize_resource_info(resource_info)

    return partition, service, region, account, maybe_resource_type, resource_id


@dataclass(frozen=True)
class ResourceTag:  # pylint: disable=too-many-instance-attributes
    account: str
    arn: str
    key: str
    partition: str
    region: str
    resource_id: str
    resource_type: str | None
    service: str
    value: str

    @staticmethod
    def from_arn(arn: str, key: str, value: str) -> ResourceTag:
        partition, service, region, account, maybe_resource_type, resource_id = (
            _parse_arn(arn)
        )

        return ResourceTag(
            account=account,
            arn=arn,
            key=key,
            partition=partition,
            region=region,
            resource_id=resource_id,
            resource_type=maybe_resource_type,
            service=service,
            value=value,
        )


@dataclass(frozen=True)
class Resource:  # pylint: disable=too-many-instance-attributes
    arn: str
    account: str
    partition: str
    resource_id: str
    service: str
    region: str
    tags: list[ResourceTag]
    resource_type: str | None

    @staticmethod
    def from_arn(arn: str, tags: list[ResourceTag]) -> Resource:
        partition, service, region, account, maybe_resource_type, resource_id = (
            _parse_arn(arn)
        )

        return Resource(
            arn=arn,
            account=account,
            partition=partition,
            resource_id=resource_id,
            service=service,
            region=region,
            tags=tags,
            resource_type=maybe_resource_type,
        )


class Resources:  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        # client: ResourceGroupsTaggingAPIClient
        client: Any,
    ) -> None:
        self.__client = client

    def retrieve_resources(self) -> list[Resource]:
        response = self.__client.get_resources(
            ResourcesPerPage=100,
            IncludeComplianceDetails=False,
            ExcludeCompliantResources=False,
        )

        resources = response["ResourceTagMappingList"]

        resources_metas: list[Resource] = []

        for resource in resources:
            tag_metas = [
                ResourceTag.from_arn(
                    resource["ResourceARN"], key=tag["Key"], value=tag["Value"]
                )
                for tag in resource["Tags"]
            ]

            resources_metas.append(
                Resource.from_arn(arn=resource["ResourceARN"], tags=tag_metas)
            )

        return resources_metas
