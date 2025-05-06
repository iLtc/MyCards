#!/bin/bash
set -e

# Check if database file exists
if [ ! -f "instance/flaskr.sqlite" ]; then
    echo "Initializing database..."
    flask init-db
fi

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
