import os
from django.core.wsgi import get_wsgi_application

# Debugging STATIC_URL
print(f"[DEBUG] STATIC_URL in wsgi.py: {os.environ.get('STATIC_URL')}")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Private_Chat.settings')

application = get_wsgi_application()