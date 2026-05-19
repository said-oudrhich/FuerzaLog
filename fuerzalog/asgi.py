"""
Configuración ASGI para el proyecto FuerzaLog.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuerzalog.settings')

application = get_asgi_application()
