from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework import status
from two_factor.views import LoginView
from django.views.generic import ListView
from .models import CustomUser  # Correct
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.urls import path
from . import views

app_name = 'chat'



@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

CustomUser = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.CustomUser

class UserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

class CustomUserListView(ListView):
    model = CustomUser
    template_name = "CustomUsers/CustomUser_list.html"

class Custom2FALoginView(LoginView):
    template_name = "registration/login.html"  # Ensure this template exists

@api_view(['POST'])
def get_tokens_for_CustomUser(request):
    data = request.data
    try:
        CustomUserInstance = CustomUser.objects.get(username=data['username'])  # Corrected field name
        refresh = RefreshToken.for_user(CustomUserInstance)  # Corrected method
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=400)

@csrf_exempt
def register_CustomUser(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            CustomUsername = data.get("CustomUsername")
            email = data.get("email")
            password = data.get("password")

            if not CustomUsername or not email or not password:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            if CustomUser.objects.filter(CustomUsername=CustomUsername).exists():
                return JsonResponse({"error": "CustomUsername already taken"}, status=400)

            CustomUser = CustomUser.objects.create_CustomUser(CustomUsername=CustomUsername, email=email, password=password)
            return JsonResponse({"message": "CustomUser registered successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('chat:lobby')  # Redirect to the chat lobby
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the chat room
            return redirect('chat:room', room_name='lobby')  # Default room is 'lobby'
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})

    # Handle GET request to render the login form
    return render(request, 'registration/login.html')

