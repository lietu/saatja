# ----- Build ----- #

# python:3.8.6-alpine3.12 on 2020-12-03
FROM python@sha256:d5d980cae51aa5dff6fe18a534e388d03ef5f76e9d001558e43c9886cb837594 AS build

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    WORKON_HOME="/.venv" \
    USER="saatja" \
    GROUP="saatja" \
    UID=1000 \
    GID=1000 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/usr/local/poetry" \
    POETRY_VERSION="1.1.4" \
    PATH="${PATH}:/.venv:/usr/local/poetry/bin"

WORKDIR /src/

COPY docker ./docker
RUN sh docker/build-prepare.sh

USER ${USER}

COPY pyproject.toml poetry.lock ./
RUN sh docker/build-setup.sh


# ----- Runtime environment ----- #

# python:3.8.6-alpine3.12 on 2020-12-03
FROM python@sha256:d5d980cae51aa5dff6fe18a534e388d03ef5f76e9d001558e43c9886cb837594 AS runtime

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    WORKON_HOME="/.venv" \
    USER="saatja" \
    GROUP="saatja" \
    UID=1000 \
    GID=1000 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/usr/local/poetry" \
    GCLOUD_VERSION="289.0.0" \
    POETRY_VERSION="1.1.4" \
    PATH="${PATH}:/.venv:/usr/local/poetry/bin:/opt/google-cloud-sdk/bin"

# Copy results from build environments
COPY --from=build ${POETRY_HOME} ${POETRY_HOME}
COPY --from=build ${WORKON_HOME} ${WORKON_HOME}

WORKDIR /src
COPY . ./
RUN sh docker/runtime-prepare.sh

USER ${USER}
EXPOSE 8080

ENTRYPOINT ["poetry", "run", "saatja"]
