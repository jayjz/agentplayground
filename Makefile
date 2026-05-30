.PHONY: help install dev build test lint format clean docker-up docker-down db-migrate db-upgrade db-downgrade

help:
	@echo "Available commands:"
	@echo "  make install      - Install all dependencies"
	@echo "  make dev          - Start development servers"
	@echo "  make build        - Build all packages"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make docker-up    - Start Docker Compose stack"
	@echo "  make docker-down  - Stop Docker Compose stack"
	@echo "  make db-migrate   - Create new migration"
	@echo "  make db-upgrade   - Apply migrations"
	@echo "  make db-downgrade - Revert last migration"

install:
	pnpm install
	cd apps/api && pip install -e ".[dev]"

dev:
	docker-compose up -d postgres redis
	@echo "Starting API and Web in development mode..."
	@echo "Run in separate terminals:"
	@echo "  cd apps/api && uvicorn app.main:app --reload"
	@echo "  cd apps/web && pnpm dev"

build:
	pnpm -r build
	cd apps/api && python -m build

test:
	cd apps/api && pytest -v
	cd apps/web && pnpm test

lint:
	cd apps/api && ruff check . && pyright
	cd apps/web && pnpm lint

format:
	cd apps/api && ruff format . && ruff check --fix .
	cd apps/web && pnpm format

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf apps/web/.next apps/web/out dist build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

db-migrate:
	cd apps/api && alembic revision --autogenerate -m "$(msg)"

db-upgrade:
	cd apps/api && alembic upgrade head

db-downgrade:
	cd apps/api && alembic downgrade -1

db-reset:
	cd apps/api && alembic downgrade base && alembic upgrade head

setup-dev: docker-up
	@echo "Waiting for services..."
	sleep 5
	make db-upgrade
	@echo "Development environment ready!"
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"
	@echo "Web: http://localhost:3000"
