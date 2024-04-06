#!/usr/bin/env bash

function cd_to_source_directory () {
  cd `dirname ${0}`/../src
}

function format () {
  echo "sorting imports: ${1}"
  p run isort --profile=black ${1}
  echo "formatting: ${1}"
  p run black ${1}
}

cd_to_source_directory

source ../bin/shared.sh

echo "Formatting modules"
format aws_meta_aggregator
format tests
echo "Formatted modules"
