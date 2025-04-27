from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('room/<path:room_name>/', views.room, name='room'),  # Use <path:room_name> to allow slashes
]
