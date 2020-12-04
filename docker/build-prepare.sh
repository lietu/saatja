#!/usr/bin/env sh
#
# WARNING!
# ========
#
# THIS FILE IS NOT USED IN RUNTIME, ONLY WHILE BUILDING DOCKER IMAGES
# DO NOT ADD ANYTHING RUNTIME OR ENVIRONMENT SPECIFIC HERE
#
# This file is for installing the larger dependencies that rarely change such
# as OS packages, utilities and so on, for the build environment
#

# shellcheck disable=SC2039
set -exuo pipefail

sh docker/create-user.sh

# Install dependencies
apk add --update --no-cache --virtual build-dependencies \
    python3-dev \
    build-base \
    linux-headers \
    gcc \
    curl \
    musl-dev

sh docker/prepare-workon-dir.sh
sh docker/install-poetry.sh

# Allow the next script to run as ${USER}
chown -R "${USER}":"${GROUP}" /src
