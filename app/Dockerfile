# Use Python 3.9 as base image
FROM python:3.9-slim

# Install PostgreSQL dependencies required for psycopg2
RUN apt-get update \
    && apt-get install -y libpq-dev gcc iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY . .

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]