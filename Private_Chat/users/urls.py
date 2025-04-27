from django.urls import path
from .views import CustomUserListView, RegisterView, register_CustomUser, get_tokens_for_CustomUser, Custom2FALoginView, signup_view, custom_login_view

urlpatterns = [
    path('list/', CustomUserListView.as_view(), name='user_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', custom_login_view, name='login'),  # Add this line
    path('register-user/', register_CustomUser, name='register_user'),
    path('token/', get_tokens_for_CustomUser, name='get_tokens_for_user'),
    path('2fa-login/', Custom2FALoginView.as_view(), name='custom_2fa_login'),
    path('signup/', signup_view, name='signup'),  # Ensure this matches the template reference
]
