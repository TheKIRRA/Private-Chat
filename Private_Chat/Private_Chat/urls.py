"""
URL configuration for Private_Chat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from users.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

def home(request):
    return HttpResponse("Welcome to Private-Chat!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Include the users app's URLs
    path('chat/', include('chat.urls')),   # Include the chat app's URLs
]
