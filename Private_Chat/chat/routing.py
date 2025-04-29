from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),  # Match WebSocket paths with /ws/chat/<room_name>/
]
print(f"[DEBUG] WebSocket URL patterns: {websocket_urlpatterns}")