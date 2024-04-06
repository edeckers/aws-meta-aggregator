# Prometheus API for AWS Meta Aggregator

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)

Aggregates information about all resources in an AWS account, and sends it to stdout

## Available Metrics

### Resource

`resource{arn="arn:aws:ec2:eu-central-1:123456789012:route-table/rtb-db06309ec8ce58bb"} 1`

### Resource Tag

`resource_tag{arn="arn:aws:ec2:eu-central-1:123456789012:route-table/rtb-db06309ec8ce58bb",tag="Name",value="MyBeautifulRouteTable"} 1`
