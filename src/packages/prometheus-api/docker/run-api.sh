#!/usr/bin/env bash

cd /app/packages/api

PROMETHEUS_API_HOST=${PROMETHEUS_API_HOST:-"0.0.0.0"}
PROMETHEUS_API_PORT=${PROMETHEUS_API_PORT:-"8000"}

python -m prometheus_api run-api \
  --host ${PROMETHEUS_API_HOST} \
  --port ${PROMETHEUS_API_PORT}