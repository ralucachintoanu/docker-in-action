FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN pip install poetry
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Run the Flask API
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]