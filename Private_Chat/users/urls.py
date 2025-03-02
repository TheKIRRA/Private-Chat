from django.urls import path
from . import views
from .views import UserListView, RegisterView, LoginView, UserView, register_user, get_tokens_for_user, Custom2FALoginView

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', get_tokens_for_user, name='token_obtain_pair'),
    path('2fa-login/', Custom2FALoginView.as_view(), name='2fa_login'),
    path('', UserListView.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserView.as_view(), name='user-detail'),
]
