FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.5.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'


RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    cmake \
    ffmpeg \
    curl \
    libgdal-dev \
    gcc \
    # Installing `poetry` package manager:
    # https://github.com/python-poetry/poetry
    && curl -sSL 'https://install.python-poetry.org' | python - \
    && poetry --version \
    # Cleaning cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    # Set timezone:
    && ln -fs /usr/share/zoneinfo/Europe/Madrid /etc/localtime \
    && echo "Europe/Madrid" > /etc/timezone

COPY poetry.lock pyproject.toml /src/

WORKDIR /src

ARG ENVIRONMENT

RUN echo "$ENVIRONMENT" && poetry --version \
  # Install deps:
  && poetry run pip install -U pip \
  && poetry install \
    $(if [ "$ENVIRONMENT" = 'production' ]; then echo '--no-dev'; fi) \
    --no-interaction --no-ansi \
  # Cleaning poetry installation's cache for production:
  && if [ "$ENVIRONMENT" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi

COPY /src/entrypoint.sh /entrypoint.sh

RUN chmod +x '/entrypoint.sh'

COPY ./src /src

CMD ["/src/entrypoint.sh"]