# Recreate the root .venv and install tools
venv:
    python3.12 -m venv .venv
    . .venv/bin/activate && pip install black pylint

# Check the format of all Python code using Black
check-format:
    black --check api etl airflow

# Format all Python code using Black
format:
    black airflow api etl

# Lint all Python code using pylint
lint:
    pylint airflow api etl

# Build the project
build:
    just venv
    just check-format    
    just lint
    # just test
    # just test-coverage
    # just start-all


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
