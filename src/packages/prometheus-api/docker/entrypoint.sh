#!/usr/bin/env bash

# inspired by https://github.com/sameersbn/docker-gitlab/blob/master/entrypoint.sh

set -e -u -o pipefail

case ${1} in
  run:uvicorn)
    /app/docker/run-api.sh
    ;;
  help)
    echo "Available options:"
    echo " run:uvicorn       - Run the API server"
    echo " help              - Displays this help"
    echo ""
    echo " [command]         - Execute the specified command, eg. bash."
    ;;
  *)
    exec "$@"
    ;;
esac
