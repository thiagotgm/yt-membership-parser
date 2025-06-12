ARG BASE_IMAGE_VERSION="3.13.4-bookworm"
ARG INSTALL_DIR="/opt/app"

FROM python:${BASE_IMAGE_VERSION} AS build

ARG INSTALL_DIR

ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 - --version 2.1.3
ENV PATH="$PATH:$POETRY_HOME/bin"

RUN poetry self add poetry-plugin-bundle@~1.7

RUN python3.13 -m venv --symlinks --without-pip ${INSTALL_DIR}

WORKDIR /work

COPY . .

RUN poetry bundle venv --only=main --compile ${INSTALL_DIR}

FROM python:${BASE_IMAGE_VERSION} AS release

ARG INSTALL_DIR

RUN apt-get update \
    && apt-get install -y tesseract-ocr=5.3.0-2 \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=root:root --from=build ${INSTALL_DIR} ${INSTALL_DIR}
COPY --chown=root:root --chmod=0755 ./docker-entrypoint.sh /opt/docker-entrypoint.sh

ENV PATH="$PATH:${INSTALL_DIR}/bin"

# Use root GID for OpenShift compatibility
RUN adduser --system --uid 150 --gid 0 --no-create-home runner

USER runner

WORKDIR /app

# Startup script
ENTRYPOINT [ "/opt/docker-entrypoint.sh" ]

EXPOSE 8000
