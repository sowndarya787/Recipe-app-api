# Use official Python 3.12 slim image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL and building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create necessary media/static directories with correct permissions
RUN mkdir -p /vol/web/media /vol/web/static

# Create non-root user
RUN addgroup --system django-user && \
    adduser --system --ingroup django-user django-user

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy entrypoint script and set permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy project files
COPY . /app/

# Set permissions
RUN chown -R django-user:django-user /vol /app && chmod -R 755 /vol

# Use non-root user
USER django-user

# Expose port
EXPOSE 8001

# Set default command
ENTRYPOINT ["/entrypoint.sh"]
