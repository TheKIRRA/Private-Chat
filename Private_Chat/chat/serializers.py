from rest_framework import serializers
from users.models import CustomUser  # Assuming CustomUser is defined in users.models

class RegisterSerializer(serializers.ModelSerializer):  # Ensure this class is correctly defined
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']
