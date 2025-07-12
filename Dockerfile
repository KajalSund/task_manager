# Use official Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Update apt and install postgresql-client for pg_isready
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app code
COPY . .

# Expose the port your app runs on (change if needed)
EXPOSE 8000

# Command to run your app (adjust if using Uvicorn/other)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
