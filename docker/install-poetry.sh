#!/usr/bin/env sh

# shellcheck disable=SC2039
set -exuo pipefail

POETRY_URL=https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py

mkdir "${POETRY_HOME}"
chown -R "${USER}":"${GROUP}" "${POETRY_HOME}"

su "${USER}" -c "curl -sSL ${POETRY_URL} -o /tmp/get-poetry.py"
su "${USER}" -c "python /tmp/get-poetry.py --version ${POETRY_VERSION}"

chmod +x "${POETRY_HOME}"/bin/*
su "${USER}" -c "python -m pip install --upgrade pip"
su "${USER}" -c "poetry config virtualenvs.in-project false"
su "${USER}" -c "poetry config virtualenvs.path ${WORKON_HOME}"
