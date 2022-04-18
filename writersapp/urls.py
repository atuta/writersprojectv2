from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashbooard, name='writers-dashboard'),
    path('logout/', views.do_logout, name='logout'),
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
    path('update-task-status/', views.view_update_task_status, name='update-task-status'),
    path('edit-task/', views.view_edit_task, name='edit-task'),
    path('edit-project/', views.view_edit_project, name='edit-project'),
    path('pending-writers-applications/', views.page_pending_applications, name='pending-writers-applications'),
    path('save-writer-application/', views.view_save_writer_application, name='save-writer-application'),
    path('save-project/', views.view_save_project, name='save-project'),
    path('add-task/<str:project_code>/', views.add_task, name='add-task'),
    path('create-project/', views.create_project, name='create-project'),
    path('writers-dashboard/', views.dashbooard, name='writers-dashboard'),
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('custom-login/', views.view_custom_login, name='custom-login'),
    path('reject-application/', views.view_reject_application, name='reject-application'),
    path('approve-application/', views.view_approve_application, name='approve-application'),
    path('upgrade-to-writer/', views.upgrade_to_writer, name='upgrade-to-writer'),
    path('create-account/', views.view_create_account, name='create-account'),
]
