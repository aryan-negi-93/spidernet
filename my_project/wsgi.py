import os
from django.core.wsgi import get_wsgi_application

# Set the settings module for the Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')

# Get the WSGI application
application = get_wsgi_application()
app = application