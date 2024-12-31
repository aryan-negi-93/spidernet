#!/bin/bash

echo "BUILD START"

# Install dependencies
python3 -m pip install --no-cache-dir -r requirements.txt

# Run database migrations
python3 manage.py migrate --noinput

# Collect static files
python3 manage.py collectstatic --noinput

echo "BUILD END"
