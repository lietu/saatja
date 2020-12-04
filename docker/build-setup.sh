#!/usr/bin/env sh
#
# WARNING!
# ========
#
# THIS FILE IS NOT USED IN RUNTIME, ONLY WHILE BUILDING DOCKER IMAGES
# DO NOT ADD ANYTHING RUNTIME OR ENVIRONMENT SPECIFIC HERE
#

# shellcheck disable=SC2039
set -exuo pipefail
poetry install --no-dev
