from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('room/<str:room_name>/', views.room, name='room'),  # Example for room view
]
