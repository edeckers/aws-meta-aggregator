#!/usr/bin/env bash

function cd_to_source_directory() {
  cd `dirname ${0}`/../src
}

function run_linter() {
  echo "linting: ${1}"
  p run pylint ${1}
  echo "sorting imports: ${1}"
  p run isort --profile=black --check-only ${1}
  echo "formatting: ${1}"
  p run black --check  ${1} --diff
  echo "check types: ${1}"
  p run mypy ${1} --ignore-missing-imports
  echo "scanning vulnerabilities: ${1}"
  p run bandit -r ${1} -s B608
}

cd_to_source_directory

source ../bin/shared.sh

echo "Running linters"
run_linter packages/aggregator-library/aws_meta_aggregator
run_linter packages/aggregator-library/tests
run_linter packages/prometheus-api/prometheus_api
echo "Finished linters"
