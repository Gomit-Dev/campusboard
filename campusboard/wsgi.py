"""
WSGI config for CampusBoard project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusboard.settings')
application = get_wsgi_application()
