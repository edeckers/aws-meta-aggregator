from aws_meta_aggregator.resources import Resource, ResourceTag


class PrometheusResourcePrinter:  # pylint: disable=too-few-public-methods
    def print(self, resource: Resource) -> None:
        # pylint: disable=line-too-long
        print(f'resource{{arn="{resource.arn}"}} 1')


class PrometheusTagsPrinter:  # pylint: disable=too-few-public-methods
    def print(self, arn: str, tags: list[ResourceTag]) -> None:
        for tag in tags:
            # pylint: disable=line-too-long
            print(
                f'resource_tag{{arn="{arn}",tag="{tag.tag}",value="{tag.value}"}} 1'
            )
