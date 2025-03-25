FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Copy script and dataset file into the container
COPY etl.py .
COPY dataset_sample.csv .

# Define the command to run the ETL script
CMD ["python", "etl.py"]