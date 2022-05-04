import json

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .reject_application import RejectApplication
from .approve_application import ApproveApplication
from .pick_task import PickTask
from .client_writer_reject import ClientWriterReject
from .client_writer_return import ClientWriterReturn
from .admin_writer_return import AdminWriterReturn
from .admin_writer_reject import AdminWriterReject
from .admin_approve_task import AdminApproveTask
from .writer_submit_task import WriterSubmitTask
from .submit_project import SubmitProject
from .update_task_status import UpdateTaskStatus
from .edit_task import EditTask
from .save_task import SaveTask
from .save_project_options import SaveProjectOptions
from .assign_task import AssignTask
from .log_task import LogTask
from .edit_project import EditProject
from .save_writer_application import SaveWriterApplication
from .admin_pay import AdminPay
from .accept_admin_approved_task import AcceptAdminApprovedTask
from .save_project import SaveProject
from .pending_admin_approvals import PendingAdminApprovals
from .my_admin_approved_tasks import MyAdminApprovedTasks
from .my_revisions import MyRevisions
from .my_drafts import MyDrafts
from .project_tasks import ProjectTasks
from .pending_writer_applications import PendingWriterApplications
from .my_projects import MyProjects
from .create_account import CreateCustomUser
from .models import Categories, Projects, Tasks, ActiveTasks, Countries, WritersApplications, \
    CustomUser, PaymentTransactions
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.db.models import Q


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


@api_view(['POST', 'GET'])
@csrf_exempt
def view_save_writer_application(request):
    email = request.user.email
    article = request.POST.get("article")
    language = request.POST.get("language")

    response = SaveWriterApplication.save_writer_application('', email, article, language)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_reject_application(request):
    application_id = request.POST.get("application_id")
    response = RejectApplication.reject_application('', application_id)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_approve_application(request):
    application_id = request.POST.get("application_id")
    response = ApproveApplication.approve_application('', application_id)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_save_project_options(request):
    task_code = request.POST.get("task_code")
    writer_level = request.POST.get("writer_level")
    extra_proofreading = request.POST.get("extra_proofreading")
    priority_order = request.POST.get("priority_order")
    favourite_writers = request.POST.get("favourite_writers")

    response = SaveProjectOptions.save_project_options('', task_code, writer_level, extra_proofreading,
                                                       priority_order, favourite_writers)
    return HttpResponse(response, content_type='text/json')


@ensure_csrf_cookie
def upload_files(request):
    if request.method == "GET":
        data = {"status": "fail", "data": {"message": "get_method_not_allowed"}}
        return HttpResponse(json.dumps(data), content_type='text/json')
    if request.method == 'POST':
        files = request.FILES.getlist('files[]', None)
        # print(files)
        for f in files:
            handle_uploaded_file(f)
        data = {"status": "success", "data": {"message": "file_uploaded"}}
        return HttpResponse(json.dumps(data), content_type='text/json')
    else:
        data = {"status": "fail", "data": {"message": "uploaded_failed"}}
        return HttpResponse(json.dumps(data), content_type='text/json')


# to go to a utility file
def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@api_view(['POST', 'GET'])
@csrf_exempt
def view_asign_task(request):
    task_code = request.POST.get("task_code")
    writer_email = request.POST.get("writer_email")

    response = AssignTask.assign_task('', task_code, writer_email)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_log_task(request):
    task_code = request.POST.get("task_code")
    article = request.POST.get("article")
    author = request.user.email

    response = LogTask.log_task('', task_code, article, author)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_pick_task(request):
    author = request.user.email
    task_code = request.POST.get("task_code")
    response = PickTask.pick_task('', task_code, author)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_client_writer_reject(request):
    task_code = request.POST.get("task_code")
    response = ClientWriterReject.client_writer_reject('', task_code)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_client_writer_return(request):
    task_code = request.POST.get("task_code")
    reason = request.POST.get("reason")
    response = ClientWriterReturn.client_writer_return('', task_code, reason)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_admin_writer_return(request):
    task_code = request.POST.get("task_code")
    reason = request.POST.get("reason")
    response = AdminWriterReturn.admin_writer_return('', task_code, reason)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_admin_writer_reject(request):
    task_code = request.POST.get("task_code")
    response = AdminWriterReject.admin_writer_reject('', task_code)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_admin_approve_task(request):
    task_code = request.POST.get("task_code")
    response = AdminApproveTask.admin_approve_task('', task_code)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_writer_submit_task(request):
    task_code = request.POST.get("task_code")
    response = WriterSubmitTask.writer_submit_task('', task_code)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_submit_project(request):
    project_code = request.POST.get("project_code")

    response = SubmitProject.submit_project('', project_code)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_update_task_status(request):
    task_code = request.POST.get("task_code")
    task_status = request.POST.get("task_status")

    response = UpdateTaskStatus.update_task_status('', task_code, task_status)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_edit_task(request):
    task_code = request.POST.get("task_code")
    task_title = request.POST.get("task_title")
    word_count = request.POST.get("word_count")
    word_count_description = request.POST.get("word_count_description")
    keywords = request.POST.get("keywords")
    keyword_repetition = request.POST.get("keyword_repetition")
    task_instructions = request.POST.get("task_instructions")
    doc = request.POST.get("doc")
    writer_level = request.POST.get("writer_level")
    extra_proofreading = request.POST.get("extra_proofreading")
    priority_order = request.POST.get("priority_order")
    favourite_writers = request.POST.get("favourite_writers")
    deadline = request.POST.get("deadline")

    response = EditTask.edit_task('', task_code, task_title, word_count, word_count_description, keywords,
                                  keyword_repetition, task_instructions, doc, writer_level, extra_proofreading,
                                  priority_order, favourite_writers, deadline)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_save_task(request):
    project_code = request.POST.get("project_code")
    task_title = request.POST.get("task_title")
    word_count = request.POST.get("word_count")
    word_count_description = request.POST.get("word_count_description")
    keywords = request.POST.get("keywords")
    keyword_repetition = request.POST.get("keyword_repetition")
    task_instructions = request.POST.get("task_instructions")
    doc = request.POST.get("doc")
    writer_level = request.POST.get("writer_level")
    extra_proofreading = request.POST.get("extra_proofreading")
    priority_order = request.POST.get("priority_order")
    favourite_writers = request.POST.get("favourite_writers")
    deadline = request.POST.get("deadline")

    task_owner = request.user.email

    response = SaveTask.save_task('', project_code, task_owner, task_title, word_count, word_count_description,
                                  keywords,
                                  keyword_repetition, task_instructions, doc, writer_level, extra_proofreading,
                                  priority_order, favourite_writers, deadline)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_edit_project(request):
    project_code = request.POST.get("project_code")
    title = request.POST.get("title")
    category = request.POST.get("category")
    language = request.POST.get("language")
    description = request.POST.get("description")

    response = EditProject.edit_project('', project_code, title, category, language, description)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_admin_pay(request):
    task_code = request.POST.get("task_code")

    response = AdminPay.admin_pay('', task_code)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_accept_admin_approved_task(request):
    task_code = request.POST.get("task_code")
    stars = request.POST.get("stars")

    response = AcceptAdminApprovedTask.accept_admin_approved_task('', task_code, stars)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_save_project(request):
    title = request.POST.get("title")
    category = request.POST.get("category")
    language = request.POST.get("language")
    description = request.POST.get("description")
    owner = request.user.email

    response = SaveProject.save_project('', title, category, language, description, owner)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_custom_login(request):
    username = request.POST.get("email")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        userole = request.user.userrole
        data = {"status": "success", "data": {"message": "login_success", "userrole": userole}}
        return HttpResponse(json.dumps(data), content_type='text/json')
    else:
        data = {"status": "fail", "data": {"message": "login_fail"}}
        return HttpResponse(json.dumps(data), content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_create_account(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    country = request.POST.get("country")
    userrole = request.POST.get("userrole")
    password = request.POST.get("password")

    response = CreateCustomUser.create_custom_user('', first_name, last_name, phone, email, country, userrole, password)
    return HttpResponse(response, content_type='text/json')


def do_task(request, task_code):
    try:
        tasks_obj = Tasks.objects.get(t_task_code=task_code)
        task_title = tasks_obj.t_title

        active_task_obj = ActiveTasks.objects.get(t_code=task_code)
        article = active_task_obj.t_article
    except ActiveTasks.DoesNotExist as e:
        article = ""

    return render(request, "do-task.html", context={"data": tasks_obj,
                                                    "page_title": task_title, "article": article})


def project_tasks(request, project_code):
    try:
        project_obj = Projects.objects.get(p_code=project_code)
        response = ProjectTasks.project_tasks_data('', project_code)
        project_title = project_obj.p_title

        writers = list(CustomUser.objects.filter(userrole='4'))
    except Projects.DoesNotExist as e:
        response = {}
        project_title = "No task found!"
    return render(request, "project-tasks.html",
                  context={"data": response, "writers": writers, "page_title": project_title})


def page_pending_admin_approvals(request):
    try:
        pending_approvals = PendingAdminApprovals.pending_admin_approvals('')
        page_title = "Pending Admin Approvals"
    except Exception as e:
        page_title = "No pending approvals found!"
    return render(request, "pending-admin-approvals.html", context={"pendings": pending_approvals,
                                                                    "page_title": page_title})


def page_my_admin_approved_tasks(request):
    try:
        email = request.user.email
        tasks = MyAdminApprovedTasks.my_admin_approved_tasks('', email)
        page_title = "Admin Approved Tasks"
    except Exception as e:
        page_title = "No tasks found!"
    return render(request, "my-admin-approved-tasks.html", context={"tasks": tasks,
                                                                    "page_title": page_title})


def page_my_drafts(request):
    try:
        email = request.user.email
        drafts = MyDrafts.my_drafts_data('', email)
        page_title = "My Drafts"
    except Exception as e:
        page_title = "No drafts found!"
    return render(request, "my-drafts.html", context={"drafts": drafts,
                                                      "page_title": page_title})


def page_pending_allocations(request):
    try:
        pending_allocations = list(Projects.objects.filter(p_status='clientsubmitted'))
        page_title = "Pending Project Allocations"
    except Exception as e:
        page_title = "No pending allocation found!"
    return render(request, "pending-allocations.html", context={"projects": pending_allocations,
                                                                "page_title": page_title})


def page_pending_applications(request):
    try:
        writers_applications = PendingWriterApplications.pending_writer_applications('')
        page_title = "Pending Writers Applications"
    except PendingWriterApplications.DoesNotExist as e:
        page_title = "No pending task found!"
    return render(request, "pending-applications.html", context={"applications": writers_applications,
                                                                 "page_title": page_title})


def page_edit_task(request, task_code):
    try:
        task_obj = Tasks.objects.get(t_task_code=task_code)
        task_title = task_obj.t_title
    except Projects.DoesNotExist as e:
        task_title = "No task found!"
    return render(request, "edit-task.html", context={"task_data": task_obj, "page_title": task_title})


def page_edit_project(request, project_code):
    try:
        project_obj = Projects.objects.get(p_code=project_code)
        project_title = project_obj.p_title
        categories = list(Categories.objects.values())
    except Projects.DoesNotExist as e:
        project_obj = ''
        project_title = "No task found!"
    return render(request, "edit-project.html", context={"project_data": project_obj, "categories": categories,
                                                         "page_title": project_title})


def upgrade_to_writer(request):
    # response = MyProjects.my_projects_data('', request.user.email)
    return render(request, "upgrade-to-writer.html", context={"page_title": "Become a Writer"})


def page_writer_pending_tasks(request):
    owner = request.user.email
    tasks_qs = Tasks.objects.filter(Q(t_status='writersubmitted') | Q(t_status='writerresubmitted'),
                                    t_allocated_to=owner)
    return render(request, "my-pending-tasks.html", context={"tasks": tasks_qs, "page_title": "My Pending Tasks"})


def page_writer_complete_tasks(request):
    owner = request.user.email
    tasks_qs = Tasks.objects.filter(t_status='complete', t_allocated_to=owner)
    return render(request, "my-complete-tasks.html", context={"tasks": tasks_qs, "page_title": "My Complete Tasks"})


def page_my_tasks(request):
    owner = request.user.email
    tasks = list(Tasks.objects.filter(t_status='adminassigned', t_allocated_to=owner))

    return render(request, "my-tasks.html", context={"tasks": tasks, "page_title": "My Allocated Tasks"})


def page_writer_wallet(request):
    email = request.user.email
    transactions_qs = PaymentTransactions.objects.filter(p_email=email).order_by('-c_datetime')
    return render(request, "writer-wallet.html", context={"page_title": "My Wallet", "transactions": transactions_qs})


def page_revision_tasks(request):
    try:
        email = request.user.email
        revisions = MyRevisions.my_revisions_data('', email)
        page_title = "My Revisions"
    except Exception as e:
        page_title = "No revisions found!"
    return render(request, "revision-tasks.html", context={"revisions": revisions, "page_title": page_title})


def page_available_tasks(request):
    tasks = list(Tasks.objects.filter(t_status='clientsubmitted'))
    return render(request, "available-tasks.html", context={"tasks": tasks, "page_title": "Available Tasks"})


def page_my_submitted_projects(request):
    email = request.user.email
    submitted = Projects.objects.filter(p_status='clientsubmitted', p_owner=email)
    return render(request, "my-submitted-projects.html", context={"submitted": submitted, "page_title": "Pending "
                                                                                                        "Projects"})


def page_my_draft_projects(request):
    email = request.user.email
    drafts = Projects.objects.filter(p_status='clientdraft', p_owner=email)
    return render(request, "my-draft-projects.html", context={"drafts": drafts, "page_title": "Draft Projects"})


def page_admin_complete_tasks(request):
    completes = Tasks.objects.filter(t_status='complete')
    return render(request, "admin-complete-tasks.html", context={"completes": completes,
                                                                     "page_title": "Complete Tasks"})


def page_admin_revision_tasks(request):
    revisions = Tasks.objects.filter(Q(t_status='adminwriterreturned') | Q(t_status='clientwriterreturned'))
    return render(request, "admin-revision-tasks.html", context={"revisions": revisions,
                                                                     "page_title": "Revision Tasks"})


def page_admin_pending_tasks(request):
    pendings = Tasks.objects.filter(Q(t_status='writersubmitted') | Q(t_status='writerresubmitted'))
    return render(request, "admin-pending-tasks.html", context={"pendings": pendings,
                                                                     "page_title": "Pending Tasks"})


def page_client_complete_projects(request):
    email = request.user.email
    complete_projects = Projects.objects.filter(p_status='complete', p_owner=email)
    return render(request, "client-complete-projects.html", context={"complete_projects": complete_projects,
                                                                     "page_title": "Complete Projects"})


def page_client_pending_projects(request):
    email = request.user.email
    pending_projects = Projects.objects.filter(p_status='pending', p_owner=email)
    return render(request, "client-pending-projects.html", context={"pending_projects": pending_projects,
                                                                    "page_title": "Pending Projects"})


def page_my_projects(request):
    response = MyProjects.my_projects_data('', request.user.email)
    return render(request, "my-projects.html", context={"data": response, "page_title": "My Projects"})


def project_wizard(request):
    categories = list(Categories.objects.values())
    return render(request, "project-wizard.html", context={"categories": categories, "page_title": "Create a Project"})


def add_task(request, project_code):
    try:
        project_obj = Projects.objects.get(p_code=project_code)
        response = ProjectTasks.project_tasks_data('', project_code)
        project_title = project_obj.p_title
    except Projects.DoesNotExist as e:
        response = {}
        project_title = "No project found!"
    return render(request, "add-task.html", context={"data": response,
                                                     "page_title": "Add a new task to the (" + project_title
                                                                   + ") project", "project_code": project_code})


def create_project(request):
    categories = list(Categories.objects.values())
    return render(request, "create-project.html", context={"categories": categories, "page_title": "Create a Project"})


def do_logout(request):
    logout(request)
    return render(request, "index.html", {})


def home(request):
    return render(request, "index.html", {})


def admin_dashboard(request):
    email = request.user.email
    non_paid_tasks_qs = Tasks.objects.filter(t_status='complete', t_paid='no')

    drafts_count = ActiveTasks.objects.filter(t_status='writerdraft').count()
    if not drafts_count:
        drafts_count = '0'

    wip_count = Tasks.objects.filter(Q(t_status='writersubmitted') | Q(t_status='writerresubmitted')).count()
    if not wip_count:
        wip_count = '0'

    revision_count = Tasks.objects.filter(Q(t_status='adminwriterreturned') | Q(t_status='clientwriterreturned')).count()
    if not revision_count:
        revision_count = '0'

    complete_count = Tasks.objects.filter(t_status='complete').count()
    if not complete_count:
        complete_count = '0'
    return render(request, "admin-dashboard.html", {"non_paids": non_paid_tasks_qs,
                                                             "drafts_count": drafts_count,
                                                             "wip_count": wip_count,
                                                             "revision_count": revision_count,
                                                             "complete_count": complete_count,
                                                             "page_title": "Admin Dashboard"})


def client_dashboard(request):
    return render(request, "client-dashboard.html", {})


def writer_dashboard(request):
    email = request.user.email
    available_tasks_qs = Tasks.objects.filter(t_status='clientsubmitted')

    drafts_count = ActiveTasks.objects.filter(t_status='writerdraft', t_author=email).count()
    if not drafts_count:
        drafts_count = '0'

    wip_count = Tasks.objects.filter(Q(t_status='writersubmitted') | Q(t_status='writerresubmitted'),
                                     t_allocated_to=email).count()
    if not wip_count:
        wip_count = '0'

    revision_count = Tasks.objects.filter(Q(t_status='adminwriterreturned') | Q(t_status='clientwriterreturned'),
                                          t_allocated_to=email).count()
    if not revision_count:
        revision_count = '0'

    complete_count = Tasks.objects.filter(t_status='complete', t_allocated_to=email).count()
    if not complete_count:
        complete_count = '0'

    available_count = Tasks.objects.filter(t_status='clientsubmitted').count()
    if not available_count:
        available_count = '0'

    return render(request, "writer-dashboard.html", context={"available_tasks": available_tasks_qs,
                                                             "drafts_count": drafts_count,
                                                             "wip_count": wip_count,
                                                             "revision_count": revision_count,
                                                             "complete_count": complete_count,
                                                             "available_count": available_count,
                                                             "page_title": "Writer Dashboard"})


def dashboard(request):
    email = request.user.email
    available_tasks_qs = Tasks.objects.filter(t_status='clientsubmitted')

    drafts_count = ActiveTasks.objects.filter(t_status='writerdraft', t_author=email).count()
    if not drafts_count:
        drafts_count = '0'

    wip_count = Tasks.objects.filter(Q(t_status='writersubmitted') | Q(t_status='writerresubmitted'),
                                     t_allocated_to=email).count()
    if not wip_count:
        wip_count = '0'

    revision_count = Tasks.objects.filter(Q(t_status='adminreturned') | Q(t_status='clientreturned'),
                                          t_allocated_to=email).count()
    if not revision_count:
        revision_count = '0'

    complete_count = Tasks.objects.filter(t_status='complete', t_allocated_to=email).count()
    if not complete_count:
        complete_count = '0'

    available_count = Tasks.objects.filter(t_status='clientsubmitted').count()
    if not available_count:
        available_count = '0'

    return render(request, "dashboard.html", context={"available_tasks": available_tasks_qs,
                                                      "drafts_count": drafts_count,
                                                      "wip_count": wip_count,
                                                      "revision_count": revision_count,
                                                      "complete_count": complete_count,
                                                      "available_count": available_count,
                                                      "page_title": "Dashboard"})


def page_my_profile(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password-change-success')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "my-profile.html", context={"page_title": "My Profile", "form": form})


def signup_page(request):
    countries = list(Countries.objects.values())
    return render(request, "signup.html", context={"countries": countries})


def password_change_success(request):
    return render(request, "password-change-success.html", context={"page_title": "Password Change Successful!"})


def login_page(request):
    logout(request)
    return render(request, "login.html", {})


def add_post(request):
    return render(request, "add-post.html", {})
