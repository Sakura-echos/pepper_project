# urls.py
from django.urls import path
from .views import register, login_user, delete_user, change_password, get_samples, create_sample, get_sample, \
    update_sample, delete_sample, logout_user, literature_delete, literature_create, literature_update, literature_list, \
    download_effusive_only, download_experimental_only, download_natural_rocks_only, download_subaerial_only, \
    download_submarine_only, download_explosive_only, download_all

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('delete/', delete_user, name='delete'),
    path('change_password/', change_password, name='change_password'),
    path('samples/', get_samples, name='sample-list'),
    path('samples/<int:sample_id>/', get_sample, name='sample-detail'),
    path('samples/create/', create_sample, name='sample-create'),
    path('samples/<int:sample_id>/update/', update_sample, name='sample-update'),
    path('samples/<int:sample_id>/delete/', delete_sample, name='sample-delete'),
    path('literature_create/', literature_create, name='literature_create'),
    path('literature_update/<int:pk>/', literature_update, name='literature_update'),
    path('literature_delete/<int:pk>/', literature_delete, name='literature_delete'),
    path('literature', literature_list, name='literature_list'),
    path('download/all/', download_all, name='download_all'),
    path('download/explosive_only/', download_explosive_only, name='download_explosive_only'),
    path('download/effusive_only/', download_effusive_only, name='download_effusive_only'),
    path('download/experimental_only/', download_experimental_only, name='download_experimental_only'),
    path('download/natural_rocks_only/', download_natural_rocks_only, name='download_natural_rocks_only'),
    path('download/subaerial_only/', download_subaerial_only, name='download_subaerial_only'),
    path('download/submarine_only/', download_submarine_only, name='download_submarine_only'),
]