# Learning Docker: Local Data Pipeline with MongoDB

## 📌 Project Overview

This project demonstrates how to build a local data pipeline using **Docker**. The pipeline automates the process of extracting data from a CSV file, transforming it using a Python ETL service, storing it in **MongoDB**, and exposing it via a **Flask API** with **Swagger UI**. **Apache Airflow** is used to schedule the ETL process, and **Mongo Express** provides a web UI to explore the stored data. Everything runs in its own separate Docker container.

## 🚀 Technologies Used

- **Docker & Docker Compose** (Containerization & Orchestration)
- **Python (Flask, Swagger, Pandas)** (ETL & API Development)
- **MongoDB** (Database)
- **Mongo Express** (Web UI for MongoDB)
- **Apache Airflow** (Workflow Automation)
- **Justfile** (Run commands easily)

## 📂 Project Structure

```
docker-in-action/
│-- etl/                  # ETL Service
│   ├── etl.py            # Extracts, transforms, and loads data into MongoDB
│   ├── Dockerfile        # Dockerfile for ETL service
│   ├── dataset_sample.csv # Dataset
│   ├── requirements.txt  # Requirements file for etl module
│
│-- api/                  # Flask API Service
│   ├── app.py            # Serves processed data
│   ├── Dockerfile        # Dockerfile for Flask API
│   ├── requirements.txt  # Requirements file for api module
│
│-- airflow/              # Airflow for ETL Scheduling
│   ├── dags/             # Airflow DAGs folder
│
│-- docker-compose.yml    # Orchestrates all services
│-- justfile              # Defines a handy way to run multiple commands
│-- README.md             # Project Documentation
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

### 2️⃣ Build and Start Containers

```sh
just start-all
```

### 3️⃣ Access Services

- **Mongo Express UI**: [http://localhost:8081](http://localhost:8081)
- **Flask API**: [http://localhost:5000](http://localhost:5000)
- **Airflow UI**: [http://localhost:8080](http://localhost:8080)

### 4️⃣ Stopping the Services

```sh
just stop-all
```