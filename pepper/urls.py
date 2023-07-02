# urls.py
from django.urls import path
from .views import register, login_user, delete_user, change_password, get_samples, create_sample, get_sample, \
    update_sample, delete_sample

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('delete/', delete_user, name='delete'),
    path('change_password/', change_password, name='change_password'),
    path('samples/', get_samples, name='sample-list'),
    path('samples/<int:sample_id>/', get_sample, name='sample-detail'),
    path('samples/create/', create_sample, name='sample-create'),
    path('samples/<int:sample_id>/update/', update_sample, name='sample-update'),
    path('samples/<int:sample_id>/delete/', delete_sample, name='sample-delete'),
]