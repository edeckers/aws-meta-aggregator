from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ResourceTag:
    tag: str
    value: str


@dataclass(frozen=True)
class Resource:
    arn: str
    tags: list[ResourceTag]


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
                ResourceTag(tag=tag["Key"], value=tag["Value"])
                for tag in resource["Tags"]
            ]

            resources_metas.append(
                Resource(arn=resource["ResourceARN"], tags=tag_metas)
            )

        return resources_metas
