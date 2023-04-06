# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:3.11-slim-bullseye AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    VENV_PATH="/app/.venv" \
    PATH="$VENV_PATH/bin:$PATH"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential curl

# Install Poetry
ARG POETRY_VERSION=1.4.2

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION} && \
    chmod a+x /opt/poetry/bin/poetry


WORKDIR /app

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
COPY poetry.lock pyproject.toml ./

##########################
# Develoment stage image #
##########################
FROM builder AS development
ENV FASTAPI_ENV=development

RUN poetry install -E all

# Copy application code
COPY ./app .

# Expose port 8000 for uvicorn
EXPOSE 8000

CMD ["uvicorn", "--reload", "--host=0.0.0.0", "--port=8000", "main:app"]

# lint stage image runs black and isort
# running in check mode means build will fail if any linting errors occur
FROM development AS lint
RUN black --config ./pyproject.toml --check app tests
RUN isort --settings-path ./pyproject.toml --recursive --check-only

# test stage image runs our unit tests with pytest and
# coverage.  Build will fail if test coverage is under 95%
FROM development AS test
RUN coverage run --rcfile ./pyproject.toml -m pytest ./tests
RUN coverage report --fail-under 95

##########################
# Production stage image #
##########################
# in only our runtime deps that were installed in the 'builder'
FROM builder AS production
ENV FASTAPI_ENV=production
RUN poetry config virtualenvs.create false
RUN poetry install -E all

COPY ./app .

# # Create user with the name poetry
RUN groupadd -g 1500 app_runner && \
    useradd -m -u 1500 -g app_runner app_runner && \
    chown -R app_runner:app_runner /app

USER app_runner

CMD [ "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
