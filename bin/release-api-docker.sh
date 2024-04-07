#!/usr/bin/env bash

function cd_to_source_directory() {
  cd $(dirname ${0})/../src
}

function build_and_publish_docker_image() {
  cd_to_source_directory

  echo "Building and publishing Docker image ghcr.io/edeckers/aws-meta-aggregator:latest"
  docker buildx build . \
    --platform linux/amd64,linux/arm64 \
    -t ghcr.io/edeckers/aws-meta-aggregator:latest \
    -f packages/prometheus-api/Dockerfile \
    --push
  echo "Built and published Docker image ghcr.io/edeckers/aws-meta-aggregator:latest"
}

build_and_publish_docker_image
