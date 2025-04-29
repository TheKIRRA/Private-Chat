from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from urllib.parse import quote, unquote
from .models import Chatroom  # Ensure this matches the model definition
from .serializers import RegisterSerializer, LoginSerializer, CustomUserSerializer  # Ensure this matches the serializers defined

@login_required
def room(request, room_name):
    # Debug log to verify the room_name
    print(f"Accessing chatroom: {room_name}")
    
    # Fetch the chatroom or return a 404 if it doesn't exist
    chatroom = get_object_or_404(Chatroom, name=room_name)
    
    # Render the room.html template with the room_name
    return render(request, 'chat/room.html', {
        'room_name': chatroom.name
    })

def chat_room(request, room_name):
    ws_url = request.GET.get('ws_url', f'ws://{request.get_host()}/ws/chat/{room_name}/')  # Default to dynamically constructed WebSocket URL
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'websocket_url': ws_url
    })

def lobby(request):
    # Example: Fetch available chatrooms from the database or define them statically
    chatrooms = [{'name': quote('general/first')}, {'name': quote('general/second')}]  # Ensure names are URL-safe
    return render(request, 'chat/lobby.html', {'chatrooms': chatrooms})  # Render the lobby page

# Create your views here.

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('<path:room_name>/', views.chat_room, name='chat_room'),
]
