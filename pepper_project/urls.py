from django.contrib import admin
from django.urls import path
from pepper import views
from django.urls import re_path
from django.urls import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('', views.home, name='home'),
    path('data_plotter/', views.data_plotter, name='data_plotter'),
    path('download_data/', views.download_data, name='download_data'),
    path('upload_new_data/', views.upload_new_data, name='upload_new_data'),
    path('polydispersivity_tool/', views.polydispersivity_tool, name='polydispersivity_tool'),
    path('literature_finder/', views.literature_finder, name='literature_finder'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('app1/', include('pepper.urls')),
    path('manage_data/', views.manage_data, name='manage_data'),
    path('samples/', views.get_samples, name='get_samples'),
]
