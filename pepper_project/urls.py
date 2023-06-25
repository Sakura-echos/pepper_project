"""
URL configuration for pepper_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from pepper import views

urlpatterns = [
    path('', views.home, name='home'),
    path('data_plotter/', views.data_plotter, name='data_plotter'),
    path('download_data/', views.download_data, name='download_data'),
    path('upload_new_data/', views.upload_new_data, name='upload_new_data'),
    path('polydispersivity_tool/', views.polydispersivity_tool, name='polydispersivity_tool'),
    path('literature_finder/', views.literature_finder, name='literature_finder'),
]
