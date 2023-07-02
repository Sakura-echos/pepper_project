# urls.py
from django.urls import path
from .views import register, login_user, delete_user, change_password

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('delete/', delete_user, name='delete'),
    path('change_password/', change_password, name='change_password'),
]