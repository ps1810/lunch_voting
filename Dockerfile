# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements/base.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app

# Create a non-root user
RUN adduser --disabled-password --no-create-home celeryuser

# Set ownership of app folder
RUN chown -R celeryuser /app

# Switch to the new user
USER celeryuser

# Start server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]