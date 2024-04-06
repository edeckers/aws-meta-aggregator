# AWS Meta Aggregator

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

Aggregates information about all resources in an AWS account

## Available Metrics

### Resource

`resource{arn="arn:aws:ec2:eu-central-1:123456789012:route-table/rtb-db06309ec8ce58bb"} 1`

### Resource Tag

`resource_tag{arn="arn:aws:ec2:eu-central-1:123456789012:route-table/rtb-db06309ec8ce58bb",tag="Name",value="MyBeautifulRouteTable"} 1`

## PromQL Examples

Retrieving all resources with a tag `Name`

`resource and on(arn) (resource_tag {tag="Name"})`

And all resources that are _missing_ a tag `Name`

`resource unless on(arn) (resource_tag {tag="Name"})`

Resources without any tags at all

`resource unless on(arn) resource_tag`

## Contributing

See the [contributing guide](CONTRIBUTING.md) to learn how to contribute to the repository and the development workflow.

## Code of Conduct

[Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

MPL-2.0
