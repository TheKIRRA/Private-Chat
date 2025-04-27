from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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

@login_required
def lobby(request):
    if request.method == 'POST':
        chatroom_name = request.POST.get('chatroomName')
        if chatroom_name:
            chatroom, created = Chatroom.objects.get_or_create(name=chatroom_name)
            return redirect('chat:room', room_name=chatroom.name)  # Redirect to the chatroom
    chatrooms = Chatroom.objects.all()
    return render(request, 'chat/lobby.html', {'chatrooms': chatrooms})

# Create your views here.

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
]
