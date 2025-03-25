[![Build](https://github.com/ralucachintoanu/docker-in-action/actions/workflows/build.yml/badge.svg)](https://github.com/ralucachintoanu/docker-in-action/actions/workflows/build.yml)

# Learning Docker: Local Data Pipeline with MongoDB

## 📌 Project Overview

This project demonstrates how to build a local data pipeline using **Docker**. The pipeline automates the process of extracting data from a CSV file, transforming it using a Python ETL service, storing it in **MongoDB**, and exposing it via a **Flask API** with **Swagger UI**. **Apache Airflow** is used to schedule the ETL process, and **Mongo Express** provides a web UI to explore the stored data. Everything runs in its own separate Docker container.

## 🚀 Technologies Used

- **Docker & Docker Compose** (Containerization & Orchestration)
- **Python** (ETL and API development with Flask, Pandas, and Swagger)
- **Poetry** (Dependency and environment management)
- **MongoDB** (Database for storing processed trip data)
- **Mongo Express** (Web UI for MongoDB)
- **Apache Airflow** (Workflow orchestration for scheduling ETL jobs)
- **Justfile** (Simplified command runner for local dev tasks and CI integration)
- **GitHub Actions** (Continuous integration pipeline for testing, linting, and formatting)

## 📂 Project Structure

```
docker-in-action/
│
│-- etl/                   # ETL Service
│   ├── etl.py             # Extracts, transforms, and loads data into MongoDB
│   ├── Dockerfile         # Dockerfile for ETL service
│   ├── dataset_sample.csv # Dataset file
│   ├── pyproject.toml     # Poetry config for etl module
│   ├── poetry.lock
│
│-- api/                   # Flask API Service
│   ├── app.py             # Serves processed data
│   ├── Dockerfile         # Dockerfile for Flask API
│   ├── pyproject.toml     # Poetry config for api module
│   ├── poetry.lock
│
│-- airflow/               # Airflow for ETL Scheduling
│   ├── dags/              # Airflow DAGs folder
│
│-- .github/               # GitHub Actions CI workflows
│   ├── workflows/         # Folder for GitHub Actions workflows
│   │   └── build.yml      # CI pipeline for building, linting, and testing
│
│-- docker-compose.yml     # Orchestrates all services
│-- justfile               # Defines a handy way to run multiple commands
│-- README.md              # Project Documentation
```

## 🔧 Setup & Usage

### 1️⃣ Create an .env file in the root folder with the following properties:

```sh
MONGO_INITDB_ROOT_USERNAME=...
MONGO_INITDB_ROOT_PASSWORD=...
MONGO_EXPRESS_USERNAME=...
MONGO_EXPRESS_PASSWORD=...
AIRFLOW_USRENAME=...
AIRFLOW_PASSWORD=...
```

### 2️⃣ Build the project (check format, run lint, tests, test coverage, ...)

```sh
just build
```

### 3️⃣ Start Containers

```sh
just start-all
```

### 4️⃣ Access Services

- **Mongo Express UI**: [http://localhost:8081](http://localhost:8081)
- **Flask API**: [http://localhost:5000](http://localhost:5000)
- **Airflow UI**: [http://localhost:8080](http://localhost:8080)

### 5️⃣ Stop Services

```sh
just stop-all
```
