import os
import sys

# Add your project directory to the Python path
path = '/home/xinjke/sentiment_platform'
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'sentiment_platform.settings'

# Create the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 