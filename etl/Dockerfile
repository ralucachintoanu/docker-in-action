FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script and dataset file into the container
COPY etl.py .
COPY dataset_sample.csv .

# Define the command to run the ETL script
CMD ["python", "etl.py"]