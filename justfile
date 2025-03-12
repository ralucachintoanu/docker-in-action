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