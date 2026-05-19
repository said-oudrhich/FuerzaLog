"""
Configuración WSGI para el proyecto FuerzaLog.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuerzalog.settings')

application = get_wsgi_application()
