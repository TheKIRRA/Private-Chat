from django.urls import path
from . import views

app_name = 'chat'  # Define the app namespace

urlpatterns = [
    path('room/<path:room_name>/', views.chat_room, name='room'),  # Use <path:room_name> to allow slashes
    path('lobby/', views.lobby, name='lobby'),  # URL pattern for lobby
]
