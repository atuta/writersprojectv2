from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashbooard, name='writers-dashboard'),
    path('logout/', views.do_logout, name='logout'),
    path('do-task/<str:task_code>/', views.do_task, name='do-task'),
    path('project-tasks/<str:project_code>/', views.project_tasks, name='project-tasks'),
    path('available-tasks/', views.page_available_tasks, name='available-tasks'),
    path('page-my-tasks/', views.page_my_tasks, name='page-my-tasks'),
    path('page-writer-wallet/', views.page_writer_wallet, name='page-writer-wallet'),
    path('pending-admin-approvals/', views.page_pending_admin_approvals, name='pending-admin-approvals'),
    path('page-my-drafts/', views.page_my_drafts, name='page-my-drafts'),
    path('page-my-projects/', views.page_my_projects, name='page-my-projects'),
    path('add-post/', views.add_post, name='add-post'),
    path('save-project-options/', views.view_save_project_options, name='save-project-options'),
    path('upload-file/', views.upload_files, name='upload-file'),
    path('page-edit-task/<str:task_code>/', views.page_edit_task, name='page-edit-task'),
    path('save-task/', views.view_save_task, name='save-task'),
    path('assign-task/', views.view_asign_task, name='assign-task'),
    path('log-task/', views.view_log_task, name='log-task'),
    path('page-edit-project/<str:project_code>/', views.page_edit_project, name='page-edit-project'),
    path('pick-task/', views.view_pick_task, name='pick-task'),
    path('accept-admin-approved-task/', views.view_accept_admin_approved_task, name='accept-admin-approved-task'),
    path('my-admin-approved-tasks/', views.page_my_admin_approved_tasks, name='my-admin-approved-tasks'),
    path('admin-approve-task/', views.view_admin_approve_task, name='admin-approve-task'),
    path('writer-submit-task/', views.view_writer_submit_task, name='writer-submit-task'),
    path('submit-project/', views.view_submit_project, name='submit-project'),
    path('update-task-status/', views.view_update_task_status, name='update-task-status'),
    path('edit-task/', views.view_edit_task, name='edit-task'),
    path('edit-project/', views.view_edit_project, name='edit-project'),
    path('pending-allocations/', views.page_pending_allocations, name='pending-allocations'),
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
