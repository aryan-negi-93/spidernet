echo = "BUILD START"
#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python3 manage.py migrate --noinput

# Collect static files
python3 manage.py collectstatic --noinput


echo = "BUILD END"
