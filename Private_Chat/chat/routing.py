from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),  # Route WebSocket connections to ChatConsumer
]

# Debug log
print("[DEBUG] WebSocket URL patterns defined:", websocket_urlpatterns)
