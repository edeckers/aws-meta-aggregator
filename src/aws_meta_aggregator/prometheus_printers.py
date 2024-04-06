from aws_meta_aggregator.resources import Resource, ResourceTag


class PrometheusResourcePrinter:  # pylint: disable=too-few-public-methods
    def print(self, resource: Resource) -> None:
        # pylint: disable=line-too-long
        print(f'resource{{resource_arn="{resource.arn}"}} 1')


class PrometheusTagsPrinter:  # pylint: disable=too-few-public-methods
    def print(self, resource_arn: str, tags: list[ResourceTag]) -> None:
        for tag in tags:
            # pylint: disable=line-too-long
            print(
                f'resource_tag{{resource_arn="{resource_arn}",tag="{tag.tag}",value="{tag.value}"}} 1'
            )
