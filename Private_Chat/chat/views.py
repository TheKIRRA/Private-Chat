from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .serializers import RegisterSerializer, LoginSerializer, CustomUserSerializer  # Ensure this matches the serializers defined

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {  # Ensure this template exists
        'room_name': room_name
    })

@login_required
def lobby(request):
    return render(request, 'chat/lobby.html')  # Ensure the template exists at this path

# Create your views here.

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
]
