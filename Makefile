.PHONY: help install train test run docker-build docker-run docker-compose-up docker-compose-down clean lint format

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

train: ## Train the model
	python src/train.py

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=app --cov=src --cov-report=html --cov-report=term-missing

run: ## Run the application
	uvicorn app:app --reload --host 0.0.0.0 --port 8000

docker-build: ## Build Docker image
	docker build -t iris-classifier .

docker-run: ## Run Docker container
	docker run -p 8000:8080 iris-classifier

docker-compose-up: ## Start services with Docker Compose
	docker-compose up -d

docker-compose-down: ## Stop services with Docker Compose
	docker-compose down

clean: ## Clean temporary files
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

lint: ## Lint code with flake8
	flake8 app.py schemas.py src/ tests/

format: ## Format code (if black/isort are installed)
	black app.py schemas.py src/ tests/
	isort app.py schemas.py src/ tests/

dvc-pull: ## Pull data and models from DVC
	dvc pull

dvc-status: ## Check DVC status
	dvc status

