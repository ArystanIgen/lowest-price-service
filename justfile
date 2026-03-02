# justfile for package-event-service project
# Run with: just <command>

# List all available commands
default:
    @just --list

# Docker Development Commands
# --------------------------
# Start all services in detached mode
up:
    docker-compose up -d

# Build all services
build:
    docker-compose build

# Build and start all services in detached mode
up-build:
    docker-compose up -d --build

# Stop all services
down args='':
    docker compose down {{ args }}

# Show logs for a specific service
logs service:
    docker-compose logs -f {{ service }}

# Restart a specific service
restart service:
    docker-compose restart {{ service }}

# Local Development Commands
# --------------------------

# Install dependencies
setup:
    uv sync

# Run the application locally
dev:
    uv run --env-file .env uvicorn app.main:main_app --reload --no-access-log --app-dir src


# Migrate data from csv file
csv-migrate:
    docker-compose run --rm -e ENV=MIGRATE_CSV fastapi

# Linting Commands
# ---------------

# Run ruff check using uv
ruff-check args='':
    uv run ruff check --no-cache . {{ args }}

# Run ruff format using uv
ruff-format:
    uv run ruff format .


# Run ty type checking
ty:
    uv run ty check

# Run bandit security check
bandit:
    uv run bandit .

# Run safety check
safety:
    uv run safety check --full-report

# Run all linting checks
lint: ruff-check ty bandit safety
    @echo "All linting checks completed"

# Run pytest tests inside Docker
test:
    docker-compose run --rm -e ENV=TEST fastapi
