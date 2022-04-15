from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashbooard, name='writers-dashboard'),
    path('do-task/<str:task_code>/', views.do_task, name='do-task'),
    path('project-tasks/<str:project_code>/', views.project_tasks, name='project-tasks'),
    path('page-my-projects/', views.page_my_projects, name='page-my-projects'),
    path('add-post/', views.add_post, name='add-post'),
    path('save-project-options/', views.view_save_project_options, name='save-project-options'),
    path('upload-file/', views.upload_files, name='upload-file'),
    path('page-edit-task/<str:task_code>/', views.page_edit_task, name='page-edit-task'),
    path('save-task/', views.view_save_task, name='save-task'),
    path('log-task/', views.view_log_task, name='log-task'),
    path('page-edit-project/<str:project_code>/', views.page_edit_project, name='page-edit-project'),
    path('edit-task/', views.view_edit_task, name='edit-task'),
    path('edit-project/', views.view_edit_project, name='edit-project'),
    path('save-project/', views.view_save_project, name='save-project'),
    path('add-task/<str:project_code>/', views.add_task, name='add-task'),
    path('create-project/', views.create_project, name='create-project'),
    path('writers-dashboard/', views.dashbooard, name='writers-dashboard'),
    path('login/', views.login_page, name='login'),
    path('custom-login/', views.view_custom_login, name='custom-login'),
    path('create-account/', views.view_create_account, name='create-account'),
]
