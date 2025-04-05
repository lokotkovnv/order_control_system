import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'order_control_system.settings'
)

application = get_wsgi_application()
