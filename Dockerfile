# Use Python 3.9+ for zoneinfo support
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create instance directory for SQLite database
RUN mkdir -p instance

# Make entrypoint script executable
RUN chmod +x docker-entrypoint.sh

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port 5000
EXPOSE 5000

# Use the entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
