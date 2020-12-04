#!/usr/bin/env sh
#
# This step is for initializing the runtime environment
#

# shellcheck disable=SC2039
set -exuo pipefail

apk add --no-cache libstdc++

# Add user
addgroup -g "${GID}" -S "${GROUP}"
adduser -u "${UID}" -S "${USER}" -G "${GROUP}" -D

# Enable su to $USER
sed -i -E "s@${USER}:(.*):/sbin/nologin@${USER}:\1:/bin/ash@" /etc/passwd

# Allow ${USER} to edit contents while installing things
chown -R "${USER}":"${GROUP}" .

# Poetry configuration
su "${USER}" -c "poetry config virtualenvs.in-project false"
su "${USER}" -c "poetry config virtualenvs.path ${WORKON_HOME}"

# Ensure user cannot edit the filesystem contents
chown -R root:root /src
