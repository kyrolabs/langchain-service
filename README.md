# LangChain Service

LangChain Service is an opinionated processing platform that allows you to develop and deploy langchain as a service with batteries included (Kong Authentication, Qdrant Vector Database, Postgresql Database, Swagger, etc.). This documentation will guide you through the installation process, as well as provide an overview of the available features and API reference.

Based on [python-poetry-docker-example](https://github.com/michael0liver/python-poetry-docker-example).

This project uses [Poetry](https://python-poetry.org/) as a dependency manager. Check out Poetry's [documentation on how to install it](https://python-poetry.org/docs/#installation) on your system before proceeding.

## Table of Contents

- [LangChain Service](#langchain-service)
  - [Table of Contents](#table-of-contents)
  - [🚀 Quick Start](#-quick-start)
  - [Dev Environment](#dev-environment)
  - [Bonus: API Specification](#bonus-api-specification)
  - [Docker](#docker)
    - [Docker Compose](#docker-compose)
  - [References and Credits](#references-and-credits)

## 🚀 Quick Start

1. create and activate a new Conda env `conda create -n langchain-service python=3.11`
2. Install Poetry (see introduction) `curl -sSL https://install.python-poetry.org | python3 -`
3. Tell Poetry to use the virtualenv python environment
   `poetry config virtualenvs.prefer-active-python true`
   `poetry shell`
4. Install dependencies `poetry install -E all`

See the [poetry docs](https://python-poetry.org/docs/) for information on how to add/update dependencies.

## Dev Environment

Start a development server locally:

```shell
poetry run uvicorn app.main:app --reload --host localhost --port 8000
```

API will be available at [localhost:8000/](http://localhost:8000/)

## Bonus: API Specification

FastAPI comes with built-in API generated documentation. Available at

- Swagger UI docs at [localhost:8000/docs](http://localhost:8000/docs)
- ReDoc docs at [localhost:8000/redoc](http://localhost:8000/redoc)

## Docker

Build images with:

```shell
docker build -t langchain-service .
```

The Dockerfile uses multi-stage builds to run lint and test stages before building the production stage.

You can stop the build at specific stages with the `--target` option with the following values: `development`, `lint`, `test`, `production`, e.g.:

```shell
docker build -t langchain-service --target $STAGE .
```

If you do not specify a target the resulting image will be the last image defined which in our case is the 'production' image.

Run the 'production' image:

```shell
docker run -it -p 8000:8000 langchain-service

```

Open your browser and go to [http://localhost:8000/redoc](http://localhost:8000/redoc) to see the API spec in ReDoc.

### Docker Compose

This project offers a complete and convenient setup using Docker Compose, allowing you to run multiple services as part of the LangChain ecosystem. Docker Compose simplifies the process of managing and organizing the various services required for a fully functional environment. In this setup, the following services are included:

- Kong: Kong serves as the API Gateway and manages authentication for the LangChain API. It acts as a reverse proxy, handling requests from clients and forwarding them to the appropriate service, while also providing authentication and other middleware features.
- Qdrant: Qdrant is a vector database that allows efficient search and retrieval of similar items based on their vector representation. It enables storing and searching for language model embeddings.
- PostgreSQL: PostgreSQL provides a robust and reliable database solution for storing and managing data associated with the LangChain API.

To build and run the containers for these services using Docker Compose, use the following command:

```shell
docker compose up
```

If you prefer to run the containers in detached mode, which means they will run in the background without displaying logs in the terminal, use the -d flag:

```shell
docker compose up -d
```

## References and Credits

- [LangChain](https://github.com/hwchase17/langchain)
- [Setting Up Qdrant with Kong for Authentication](https://medium.com/@stephane.busso/setting-up-qdrant-with-kong-for-authentication-a-step-by-step-guide-91c206a913f8)
- [Langchain NotionDBLoader](https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/notiondb.html)
- [Poetry Docker example from Michael Oliver](https://github.com/michael0liver/python-poetry-docker-example)
