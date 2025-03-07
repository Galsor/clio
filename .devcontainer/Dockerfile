# .devcontainer/Dockerfile
FROM mcr.microsoft.com/vscode/devcontainers/python:3.12

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
&& export DEBIAN_FRONTEND=noninteractive \
&& apt-get -y install git

WORKDIR /workspace

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

COPY ./pyproject.toml /workspace/
COPY ./uv.lock /workspace/

RUN uv sync --frozen