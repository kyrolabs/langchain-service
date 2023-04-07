.PHONY: dev prod build-docker

# Variables
HOST := localhost
PORT := 8000

# Development server
dev:
	@echo "Starting development server..."
	@poetry run uvicorn app.main:app --reload --host $(HOST) --port $(PORT)

# Production server
prod:
	@echo "Starting production server..."
	@poetry install --no-dev
	@poetry run uvicorn app.main:a

# Ingest data
ingest:
	@echo "Ingesting data..."
	@poetry run python app/ingest.py

# Docker build
build-docker:
	@echo "Building Docker image..."
	@docker build -t langchain-service .
