from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='writers-home'),
    path('add-post/', views.add_post, name='add-post'),
    path('create-project/', views.create_project, name='create-project'),
    path('writers-dashboard/', views.dashbooard, name='writers-dashboard'),
    path('login/', views.login, name='login'),
    path('custom-login/', views.view_custom_login, name='custom-login'),
    path('create-account/', views.view_create_account, name='create-account'),
]
