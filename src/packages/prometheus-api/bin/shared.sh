function try_source_env() {
  if [ -n "${POETRY_HOME-}" ]; then
    export PATH="${POETRY_HOME}/bin:${PATH}"
    return
  fi

  export PATH="$HOME/.local/bin:$PATH"
}

function poetry_path() {
  echo $(command -v poetry 2>/dev/null)
}

function assert_poetry_exists() {
  if [ -z $(poetry_path) ]; then
    echo "Poetry could not be found. See https://python-poetry.org/docs/"
    exit 2
  fi
}

function install_poetry() {
  if [ -z $(poetry_path) ]; then
    curl -sSL https://install.python-poetry.org/ | python -
  fi

  try_source_env
}

function p() {
  try_source_env

  assert_poetry_exists

  $(poetry_path) ${@}
}
