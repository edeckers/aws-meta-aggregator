from aws_meta_aggregator.resources import Resource, ResourceTag


class PrometheusResourcePrinter:  # pylint: disable=too-few-public-methods
    def print(self, resource: Resource) -> str:
        return f'resource{{arn="{resource.arn}"}} 1'


class PrometheusTagsPrinter:  # pylint: disable=too-few-public-methods
    def print(self, arn: str, tags: list[ResourceTag]) -> str:
        output = []
        for tag in tags:
            # pylint: disable=line-too-long
            output.append(
                f'resource_tag{{arn="{arn}",tag="{tag.tag}",value="{tag.value}"}} 1'
            )

        return "\n".join(output)
