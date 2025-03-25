# Recreate the root .venv and install tools
setup:
    bash -c 'python3.12 -m venv .venv && source .venv/bin/activate && pip install poetry black pylint pytest pytest-cov && cd api && poetry install && cd ../etl && poetry install'

# Check the format of all Python code using Black
check-format:
    bash -c 'source .venv/bin/activate && black --check api etl airflow'

# Format all Python code using Black
format:
    bash -c 'source .venv/bin/activate && black api etl airflow'

# Lint all Python code using pylint
lint:
    bash -c 'source .venv/bin/activate && pylint api etl airflow'

# Tests for the api module
test-api:
    bash -c 'source .venv/bin/activate && cd api && poetry run pytest && poetry run pytest --cov=api --cov-report=term-missing'

# Tests for the etl module
test-etl:
    bash -c 'source .venv/bin/activate && cd etl && poetry run pytest && poetry run pytest --cov=etl --cov-report=term-missing'     

# Build the project
build:
    just setup
    just check-format
    just lint
    just test-api
    just test-etl


# Starts all services
start-all:
    docker-compose up --build -d

# Stops all services
stop-all:
    docker-compose down --remove-orphans

# Restart everything (stops, rebuilds, and starts all services)
restart-all:
    docker-compose down --remove-orphans
    docker-compose build
    docker-compose up -d

# Restart only API service (stops, rebuilds, and starts it)
restart-api:
    docker-compose stop api
    docker-compose build api
    docker-compose up -d api

# Restart only ETL service (stops, rebuilds, and starts it)
restart-etl:
    docker-compose stop etl
    docker-compose build etl
    docker-compose up -d etl

# Restart only Airflow service (stops, rebuilds, and starts it)
restart-airflow:
    docker-compose stop airflow
    docker-compose build airflow
    docker-compose up -d airflow
