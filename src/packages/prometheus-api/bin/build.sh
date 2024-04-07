#!/usr/bin/env bash

set -e -o pipefail

function cd_to_root_directory() {
  cd $(dirname ${0})/..
}

function nuke_tmp() {
  echo "Nuking tmp"
  rm -rf .tmp
  echo "Nuked tmp"
}

function nuke_dist() {
  echo "Nuking dist"
  rm -rf dist/
  nuke_tmp
  echo "Nuked dist"
}

function create_build_dir() {
  echo "Creating build dir"

  mkdir .tmp
  mkdir -p dist/libs

  # We want 'develop = true' in our relative dependencies when in _dev mode_,
  # so we always use the current state of each dependency and not some
  # stale older version that needs a Poetry update on each change.
  #
  # But when we _build_ the package, we want to use deep copies of said
  # dependencies. It seems like you can't have it both ways in Poetry :(
  p export \
    --only main \
    --without-hashes \
    --format=requirements.txt > .tmp/requirements.txt
  
  p run pip install \
    -r .tmp/requirements.txt \
    --target dist/libs

  # Keep package small, remove unnecessary files
  find . -type d -name "__pycache__" | xargs rm -rf {}

  cp -r prometheus_api dist/

  nuke_tmp
  echo "Created build dir"
}

cd_to_root_directory

source bin/shared.sh

install_poetry
nuke_dist
nuke_tmp
create_build_dir
