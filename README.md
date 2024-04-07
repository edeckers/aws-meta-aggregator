# AWS Meta Aggregator

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

Aggregates information about all resources in an AWS account

## Configuration

### Watch your cardinality

:warning: Make sure you understand the implications of enabling identifier labels before doing so :warning:

When you're looking to filter on high-cardinality identifiers, Prometheus is probably not the solution you're looking for. Relevant blogpost: https://www.robustperception.io/cardinality-is-key

> Some particular things to watch out for are breaking out metrics with labels per customer. This usually works okay when you've tens of customers, but when you get into the hundreds and later thousands this tends not to end well.
>
> (...)
>
> As a general rule of thumb I'd avoid having any metric whose cardinality on a /metrics could potentially go over 10 due to growth in label values.

### Add labels to allowlist

Add space separated label names to the `PROMETHEUS_API_RESOURCE_LABEL_ALLOWLIST` and `PROMETHEUS_API_RESOURCE_TAG_LABEL_ALLOWLIST` environment variables for the labels you want to include in your results.

## Available Metrics

### Resource

`resource{arn="arn:aws:ec2:eu-central-1:123456789012:subnet/subnet-db06309ec8ce58bb",account="123456789012",partition="aws",id="subnet-db06309ec8ce58bb",service="ec2",region="eu-central-1",type="subnet"} 1`

### Resource Tag

`resource_tag{arn="arn:aws:ec2:eu-central-1:123456789012:subnet/subnet-db06309ec8ce58bb",key="Name",value="MyFavoriteSubnet",account="123456789012",partition="aws",resource_id="subnet-db06309ec8ce58bb",service="ec2",region="eu-central-1",resource_type="subnet"} 1`

## PromQL Examples

Retrieving all resources with a tag `Name`

`resource and on(arn) (resource_tag {key="Name"})`

And all resources that are _missing_ a tag `Name`

`resource unless on(arn) (resource_tag {key="Name"})`

Resources without any tags at all

`resource unless on(arn) resource_tag`

## Contributing

See the [contributing guide](CONTRIBUTING.md) to learn how to contribute to the repository and the development workflow.

## Code of Conduct

[Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

MPL-2.0
