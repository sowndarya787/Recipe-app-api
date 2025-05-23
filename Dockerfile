# Use official Python 3.12 slim image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app1

# Install system dependencies (for sqlite and general tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project code to the working directory
COPY . /app1/

# Expose the port the Django app runs on
EXPOSE 8000

# Run migrations and start the Django development server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
