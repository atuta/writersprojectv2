import json
import datetime
import time

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .mark_all_as_read import MarkAllAsRead
from .reject_application import RejectApplication
from .save_email_template import SaveEmailTemplate
from .save_cost_settings import SaveCostSettings
from .approve_application import ApproveApplication
from .admin_withdraw_task import AdminWithdrawTask
from .admin_reavail_task import AdminRevailTask
from .pick_task import PickTask
from .mark_as_read import MarkAsRead
from .send_site_message import SendSiteMessage
from .send_message import SendMessage
from .client_writer_reject import ClientWriterReject
from .client_writer_return import ClientWriterReturn
from .admin_writer_return import AdminWriterReturn
from .admin_writer_reject import AdminWriterReject
from .admin_approve_task import AdminApproveTask
from .writer_submit_appraisal_task import WriterSubmitAppraisalTask
from .writer_submit_task import WriterSubmitTask
from .wallet_submit_project import WalletSubmitProject
from .submit_project import SubmitProject
from .update_task_status import UpdateTaskStatus
from .edit_task import EditTask
from .save_appraisal_task import SaveAppraisalTask
from .save_task import SaveTask
from .save_project_options import SaveProjectOptions
from .admin_avail_task import AdminAvailTask
from .assign_task import AssignTask
from .log_task import LogTask
from .edit_project import EditProject
from .save_writer_application import SaveWriterApplication
from .admin_pay import AdminPay
from .accept_admin_approved_task import AcceptAdminApprovedTask
from .save_admin_settings import SaveAdminSettings
from .save_project import SaveProject
from .pending_admin_approvals import PendingAdminApprovals
from .my_admin_approved_tasks import MyAdminApprovedTasks
from .my_revisions import MyRevisions
from .my_drafts import MyDrafts
from .project_tasks import ProjectTasks
from .topup_wallet import TopupWallet
from .pending_writer_applications import PendingWriterApplications
from .my_projects import MyProjects
from .update_user_archive_status import UpdateUserArchiveStatus
from .update_user_status import UpdateUserStatus
from .create_admin import CreateAdmin
from .reset_password import ResetPassword
from .send_password_reset_code import SendPasswordResetCode
from .create_account import CreateCustomUser
from .models import Categories, Projects, Tasks, ActiveTasks, Countries, WritersApplications, \
    CustomUser, PaymentTransactions, Configs, EmailTemplates, ApprisalTasks, Messages, Costs, FavoriteWriters
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.db.models import Q, Sum


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
def view_send_site_message(request):
    from_email = request.POST.get("from_email")
    from_name = request.POST.get("from_name")
    subject = request.POST.get("message_subject")
    body = request.POST.get("message_body")

    response = SendSiteMessage.send_site_message('', from_email, from_name, subject, body)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_send_message(request):
    from_email = request.user.email
    to_email = request.POST.get("to_email")
    subject = request.POST.get("message_subject")
    body = request.POST.get("message_body")

    response = SendMessage.send_message('', from_email, to_email, subject, body)
    return HttpResponse(response, content_type='text/json')


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
def view_admin_avail_task(request):
    task_code = request.POST.get("task_code")
    admin_payout = request.POST.get("admin_payout")
    deadline = request.POST.get("deadline")

    response = AdminAvailTask.admin_avail_task('', task_code, admin_payout, deadline)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_asign_task(request):
    task_code = request.POST.get("task_code")
    user_id = request.POST.get("user_id")
    admin_payout = request.POST.get("admin_payout")
    deadline = request.POST.get("deadline")

    response = AssignTask.assign_task('', task_code, user_id, admin_payout, deadline)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_log_task(request):
    task_code = request.POST.get("task_code")
    article = request.POST.get("article")
    words = request.POST.get("words")
    author = request.user.email

    response = LogTask.log_task('', task_code, article, words, author)
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
    article = request.POST.get("article")
    response = AdminApproveTask.admin_approve_task('', task_code, article)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_writer_submit_appraisal_task(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    language = request.user.preferred_language
    country = request.user.country
    article = request.POST.get("article")
    article_words = request.POST.get("article_words")

    response = WriterSubmitAppraisalTask.writer_submit_appraisal_task('', first_name, last_name, email, article,
                                                                      article_words, language, country)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_writer_submit_task(request):
    task_code = request.POST.get("task_code")
    response = WriterSubmitTask.writer_submit_task('', task_code)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_wallet_submit_project(request):
    project_code = request.POST.get("project_code")
    response = WalletSubmitProject.wallet_submit_project('', project_code)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_submit_project(request):
    project_code = request.POST.get("project_code")

    response = SubmitProject.submit_project('', project_code)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_update_user_archive_status(request):
    email = request.POST.get("email")
    status = request.POST.get("status")

    response = UpdateUserArchiveStatus.update_user_archive_status('', email, status)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_update_user_status(request):
    email = request.POST.get("email")
    status = request.POST.get("status")

    response = UpdateUserStatus.update_user_status('', email, status)
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
def view_save_appraisal_task(request):
    task_code = request.POST.get("task_code")
    task_category = request.POST.get("task_category")
    task_title = request.POST.get("task_title")
    word_count = request.POST.get("word_count")
    word_count_description = request.POST.get("word_count_description")
    keywords = request.POST.get("keywords")
    keyword_repetition = request.POST.get("keyword_repetition")
    task_instructions = request.POST.get("task_instructions")

    response = SaveAppraisalTask.save_appraisal_task('', task_code, task_category, task_title, word_count,
                                                     word_count_description, keywords, keyword_repetition,
                                                     task_instructions)
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
    favourite = request.POST.get("favourite")

    response = AcceptAdminApprovedTask.accept_admin_approved_task('', task_code, stars, favourite)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_save_admin_settings(request):
    words_per_hour = request.POST.get("words_per_hour")
    buffer_in_hours = request.POST.get("buffer_in_hours")

    response = SaveAdminSettings.save_admin_settings('', words_per_hour, buffer_in_hours)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_mark_all_as_read(request):
    response = MarkAllAsRead.mark_all_as_read('')
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_mark_as_read(request):
    message_code = request.POST.get("message_code")
    response = MarkAsRead.mark_as_read('', message_code)
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

    username = username.replace(' ', '')
    password = password.replace(' ', '')

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
def view_create_admin(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    country = request.POST.get("country")

    response = CreateAdmin.create_admin('', first_name, last_name, phone, email, country)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_admin_withdraw_task(request):
    task_code = request.POST.get("task_code")
    response = AdminWithdrawTask.admin_withdraw_task('', task_code)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_save_cost_settings(request):
    basic = request.POST.get("basic")
    standard = request.POST.get("standard")
    expert = request.POST.get("expert")
    extra_proofreading = request.POST.get("extra_proofreading")
    priority_order = request.POST.get("priority_order")
    payout_perc = request.POST.get("payout_perc")

    response = SaveCostSettings.save_cost_settings('', basic, standard, expert, extra_proofreading, priority_order,
                                                   payout_perc)
    return HttpResponse(response, content_type='text/json')


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
    language = request.POST.get("language")
    if not language:
        language = 'EN-US'

    response = CreateCustomUser.create_custom_user('', first_name, last_name, phone, email, country, language,
                                                   userrole, password)
    return HttpResponse(response, content_type='text/json')


@login_required
def do_appraisal_task(request):
    try:
        user_obj = CustomUser.objects.get(email=request.user.email)

        seconds_now = (time.time())
        appraisal_task_deadline = user_obj.appraisal_task_deadline

        if appraisal_task_deadline is None or appraisal_task_deadline == '':
            user_obj.appraisal_task_deadline = ((seconds_now + (5 * 60 * 60)) * 1000)  # add 5 hours
            user_obj.save()

        task_obj = ApprisalTasks.objects \
            .get(t_task_code='833315adbf6a5d983f3fbbd431f5d515409eca116f516e4a6d811b7ca9ce2469')
        task_title = task_obj.t_title
        article = ""
    except ApprisalTasks.DoesNotExist as e:
        task_obj = ""
        task_title = "No appraisal task"
        article = ""
    try:
        user_obj2 = CustomUser.objects.get(email=request.user.email)
        appraisal_dealine = user_obj2.appraisal_task_deadline

        if not appraisal_dealine:
            appraisal_dealine = 0

        seconds_remaining = (float(appraisal_dealine) / 1000) - float(seconds_now)

        if float(seconds_remaining) > 1:
            appraisal_status = 'active'
        else:
            appraisal_status = 'expired'
    except Exception as e:
        appraisal_dealine = ''
        appraisal_status = ''
    return render(request, "do-appraisal-task.html", context={"task": task_obj,
                                                              "page_title": "Appraisal Task", "tag": "appraisal",
                                                              "appraisal_status": appraisal_status,
                                                              "appraisal_dealine": float(appraisal_dealine)})


@login_required
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


@login_required
def project_tasks(request, project_code):
    try:
        project_obj = Projects.objects.get(p_code=project_code)
        response = ProjectTasks.project_tasks_data('', project_code)
        project_title = project_obj.p_title
        client_email = project_obj.p_owner

        favourites_qs = FavoriteWriters.objects.filter(f_client_email=client_email)

        writers = list(CustomUser.objects.filter(userrole='4', is_verified='yes', is_active=True,
                                                 writer_article='yes', is_archived='no')
                       .order_by('-rating_stars'))
    except Projects.DoesNotExist as e:
        response = {}
        project_title = "No task found!"
    return render(request, "project-tasks.html",
                  context={"data": response, "writers": writers,
                           "favourites": favourites_qs, "page_title": project_title})


@login_required
def page_task_article(request, task_code):
    try:
        task_obj = Tasks.objects.get(t_task_code=task_code)
        article_obj = ActiveTasks.objects.get(t_code=task_code)
        article = article_obj
        page_title = "Task Article"
        task_title = task_obj.t_title
    except Exception as e:
        task_title = ''
        article = ''
        page_title = "No article found!"
    return render(request, "task-article.html", context={"article": article, "task_title": task_title,
                                                         "page_title": page_title})


@login_required
def page_pending_admin_approvals(request):
    try:
        pending_approvals = PendingAdminApprovals.pending_admin_approvals('')
        page_title = "Pending Task Approvals"
    except Exception as e:
        page_title = "No pending approvals found!"
    return render(request, "pending-admin-approvals.html", context={"pendings": pending_approvals,
                                                                    "page_title": page_title})


@login_required
def page_my_admin_approved_tasks(request):
    try:
        email = request.user.email
        tasks = MyAdminApprovedTasks.my_admin_approved_tasks('', email)
        page_title = "Admin Approved Tasks"
    except Exception as e:
        page_title = "No tasks found!"
    return render(request, "my-admin-approved-tasks.html", context={"tasks": tasks,
                                                                    "page_title": page_title})


@login_required
def page_admin_drafts(request):
    try:
        drafts_qs = Tasks.objects.filter(t_status='writerdraft')
        page_title = "Admin Drafts"
    except Exception as e:
        page_title = "No drafts found!"
    return render(request, "admin-drafts.html", context={"drafts": drafts_qs,
                                                         "page_title": page_title})


@login_required
def page_my_drafts(request):
    try:
        email = request.user.email
        drafts = MyDrafts.my_drafts_data('', email)
        page_title = "My Drafts"
    except Exception as e:
        page_title = "No drafts found!"
    return render(request, "my-drafts.html", context={"drafts": drafts,
                                                      "page_title": page_title})


@login_required
def page_admin_pending_projects(request):
    try:
        pending_allocations = list(Projects.objects.filter(p_status='pending'))
        page_title = "Admin Pending Projects"
    except Exception as e:
        page_title = "No pending projects found!"
    return render(request, "admin-pending-projects.html", context={"projects": pending_allocations,
                                                                   "page_title": page_title})


@login_required
def page_pending_task_allocations(request):
    try:
        pending_task_allocations = Tasks.objects.filter(t_status='clientsubmitted')
        writers = CustomUser.objects.filter(userrole='4', is_verified='yes', is_active=True,
                                                 writer_article='yes', is_archived='no').order_by('-rating_stars')
        page_title = "Pending Task Allocations"
    except Exception as e:
        pending_task_allocations = ''
        writers = ''
        page_title = "No pending task allocation!"
    return render(request, "pending-task-allocations.html", context={"tasks": pending_task_allocations,
                                                                     "writers": writers,
                                                                     "page_title": page_title})


@login_required
def page_pending_allocations(request):
    try:
        pending_allocations = list(Projects.objects.filter(p_status='clientsubmitted'))
        page_title = "Pending Project Allocations"
    except Exception as e:
        page_title = "No pending allocation found!"
    return render(request, "pending-allocations.html", context={"projects": pending_allocations,
                                                                "page_title": page_title})


@login_required
def page_pending_applications(request):
    try:
        writers_applications = PendingWriterApplications.pending_writer_applications('')
        page_title = "Pending Writers Applications"
    except PendingWriterApplications.DoesNotExist as e:
        page_title = "No pending task found!"
    return render(request, "pending-applications.html", context={"applications": writers_applications,
                                                                 "page_title": page_title})


@login_required
def page_edit_task(request, task_code):
    try:
        task_obj = Tasks.objects.get(t_task_code=task_code)
        task_title = task_obj.t_title
    except Projects.DoesNotExist as e:
        task_title = "No task found!"
    return render(request, "edit-task.html", context={"task_data": task_obj, "page_title": task_title})


@login_required
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


@login_required
def upgrade_to_writer(request):
    # response = MyProjects.my_projects_data('', request.user.email)
    return render(request, "upgrade-to-writer.html", context={"page_title": "Become a Writer"})


@login_required
def page_admin_client_draft_projects(request):
    projects_qs = Projects.objects.filter(p_status='clientdraft')
    return render(request, "admin-client-draft-projects.html", context={"projects": projects_qs,
                                                                        "page_title": "Draft Projects"})


@login_required
def page_client_completed_tasks(request):
    owner = request.user.email
    tasks_qs = Tasks.objects.filter(t_status='complete', t_owner=owner)
    return render(request, "client-completed-tasks.html", context={"tasks": tasks_qs,
                                                                   "page_title": "My Complete Tasks"})


@login_required
def page_client_revision_tasks(request):
    owner = request.user.email
    tasks_qs = Tasks.objects.filter(t_status='clientwriterreturned', t_owner=owner)
    return render(request, "client-revision-tasks.html", context={"tasks": tasks_qs, "page_title": "My Revision Tasks"})


@login_required
def page_client_pending_tasks(request):
    owner = request.user.email
    tasks_qs = Tasks.objects.filter(t_status='clientsubmitted', t_owner=owner)
    return render(request, "client-pending-tasks.html", context={"tasks": tasks_qs, "page_title": "My Pending Tasks"})


@login_required
def page_writer_pending_tasks(request):
    owner = request.user.email
    tasks_qs = Tasks.objects.filter(Q(t_status='writersubmitted') | Q(t_status='writerresubmitted')
                                    | Q(t_status='adminwriterapproved'),
                                    t_allocated_to=owner)
    return render(request, "my-pending-tasks.html", context={"tasks": tasks_qs, "page_title": "My Pending Tasks"})


@login_required
def page_writer_complete_tasks(request):
    owner = request.user.email
    tasks_qs = Tasks.objects.filter(t_status='complete', t_allocated_to=owner)
    return render(request, "my-complete-tasks.html", context={"tasks": tasks_qs, "page_title": "My Complete Tasks"})


@login_required
def page_my_tasks(request):
    owner = request.user.email
    tasks = list(Tasks.objects.filter(t_status='adminassigned', t_allocated_to=owner))

    return render(request, "my-tasks.html", context={"tasks": tasks, "page_title": "My Allocated Tasks"})


@login_required
def page_client_wallet(request):
    email = request.user.email
    transactions_qs = PaymentTransactions.objects.filter(p_email=email).order_by('-c_datetime')
    return render(request, "client-wallet.html", context={"page_title": "My Wallet", "transactions": transactions_qs})


@login_required
def page_admin_wallet(request):
    email = request.user.email
    transactions_qs = PaymentTransactions.objects.filter(p_email=email).order_by('-c_datetime')
    return render(request, "admin-wallet.html", context={"page_title": "Admin Wallet", "transactions": transactions_qs})


@login_required
def page_writer_wallet(request):
    email = request.user.email
    transactions_qs = PaymentTransactions.objects.filter(p_email=email).order_by('-c_datetime')
    return render(request, "writer-wallet.html", context={"page_title": "My Wallet", "transactions": transactions_qs})


@login_required
def page_revision_tasks(request):
    try:
        email = request.user.email
        revisions = MyRevisions.my_revisions_data('', email)
        page_title = "My Revisions"
    except Exception as e:
        page_title = "No revisions found!"
    return render(request, "revision-tasks.html", context={"revisions": revisions, "page_title": page_title})


@login_required
def page_available_tasks(request):
    tasks = list(Tasks.objects.filter(t_status='adminsubmitted'))
    return render(request, "available-tasks.html", context={"tasks": tasks, "page_title": "Available Tasks"})


@login_required
def page_my_submitted_projects(request):
    email = request.user.email
    submitted = Projects.objects.filter(p_status='clientsubmitted', p_owner=email)
    return render(request, "my-submitted-projects.html", context={"submitted": submitted, "page_title": "Pending "
                                                                                                        "Projects"})


@login_required
def page_my_draft_projects(request):
    email = request.user.email
    drafts = Projects.objects.filter(p_status='clientdraft', p_owner=email)
    return render(request, "my-draft-projects.html", context={"drafts": drafts, "page_title": "Draft Projects"})


@login_required
def page_admin_draft_tasks(request):
    drafts = Tasks.objects.filter(t_status='writerdraft')
    return render(request, "admin-draft-tasks.html", context={"drafts": drafts,
                                                              "page_title": "Draft Tasks"})


@login_required
def page_admin_complete_tasks(request):
    completes = Tasks.objects.filter(t_status='complete')
    return render(request, "admin-complete-tasks.html", context={"completes": completes,
                                                                 "page_title": "Complete Tasks"})


@login_required
def page_admin_revision_tasks(request):
    revisions = Tasks.objects.filter(Q(t_status='adminwriterreturned') | Q(t_status='clientwriterreturned'))
    return render(request, "admin-revision-tasks.html", context={"revisions": revisions,
                                                                 "page_title": "Revision Tasks"})


@login_required
def page_admin_pending_tasks(request):
    pendings = Tasks.objects.filter(Q(t_status='writersubmitted') | Q(t_status='writerresubmitted'))
    return render(request, "admin-pending-tasks.html", context={"pendings": pendings,
                                                                "page_title": "Pending Tasks"})


@login_required
def page_client_complete_projects(request):
    email = request.user.email
    complete_projects = Projects.objects.filter(p_status='complete', p_owner=email)
    return render(request, "client-complete-projects.html", context={"complete_projects": complete_projects,
                                                                     "page_title": "Complete Projects"})


@login_required
def page_client_pending_projects(request):
    email = request.user.email
    pending_projects = Projects.objects.filter(Q(p_status='pending') | Q(p_status='clientsubmitted'), p_owner=email)
    return render(request, "client-pending-projects.html", context={"pending_projects": pending_projects,
                                                                    "page_title": "Pending Projects"})


@login_required
def page_my_projects(request):
    response = MyProjects.my_projects_data('', request.user.email)
    return render(request, "my-projects.html", context={"data": response, "page_title": "My Projects"})


@login_required
def project_wizard(request):
    categories = list(Categories.objects.values())
    return render(request, "project-wizard.html", context={"categories": categories, "page_title": "Create a Project"})


@login_required
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


@login_required
def create_project(request):
    categories = list(Categories.objects.values())
    return render(request, "create-project.html", context={"categories": categories, "page_title": "Create a Project"})


def do_logout(request):
    logout(request)
    return render(request, "index.html", {})


def home(request):
    return render(request, "index.html", {})


@login_required
def admin_dashboard(request):
    email = request.user.email
    non_paid_tasks_qs = Tasks.objects.filter(t_status='complete', t_paid='no')

    drafts_count = Tasks.objects.filter(t_status='writerdraft').count()
    if not drafts_count:
        drafts_count = '0'

    wip_count = Tasks.objects.filter(Q(t_status='writersubmitted') | Q(t_status='writerresubmitted')).count()
    if not wip_count:
        wip_count = '0'

    revision_count = Tasks.objects.filter(
        Q(t_status='adminwriterreturned') | Q(t_status='clientwriterreturned')).count()
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


@login_required
def client_dashboard(request):
    email = request.user.email

    drafts_count = Projects.objects.filter(p_status='clientdraft', p_owner=email).count()
    if not drafts_count:
        drafts_count = '0'

    wip_count = Tasks.objects.filter(t_status='clientsubmitted', t_owner=email).count()
    if not wip_count:
        wip_count = '0'

    revision_count = Tasks.objects.filter(t_status='clientwriterreturned', t_owner=email).count()
    if not revision_count:
        revision_count = '0'

    complete_count = Tasks.objects.filter(t_status='complete', t_owner=email).count()
    if not complete_count:
        complete_count = '0'

    pending_qs = Tasks.objects.filter(Q(t_status='clientsubmitted') | Q(t_status='pending'), t_owner=email)
    return render(request, "client-dashboard.html", context={
        "drafts_count": drafts_count,
        "wip_count": wip_count,
        "revision_count": revision_count,
        "complete_count": complete_count,
        "pendings": pending_qs,
        "page_title": "Dashboard"})


@login_required
def writer_dashboard(request):
    email = request.user.email
    available_tasks_qs = Tasks.objects.filter(t_status='adminsubmitted')

    drafts_count = Tasks.objects.filter(t_status='writerdraft', t_allocated_to=email).count()
    if not drafts_count:
        drafts_count = '0'

    wip_count = Tasks.objects.filter(Q(t_status='writersubmitted') | Q(t_status='writerresubmitted')
                                     | Q(t_status='adminwriterapproved'),
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


@login_required
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


@login_required
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


def writer_signup_page(request):
    countries = Countries.objects.values().order_by('c_name')
    configs_qs = Configs.objects.filter(~Q(buffer_in_hours=''), ~Q(words_per_hour='')).first()
    article_title = configs_qs.signup_article_title
    return render(request, "writer-signup.html", context={"countries": countries, "article_title": article_title})


def signup_page(request):
    countries = list(Countries.objects.values())
    return render(request, "signup.html", context={"countries": countries})


def password_change_success(request):
    return render(request, "password-change-success.html", context={"page_title": "Password Change Successful!"})


@login_required
def topup_complete(request):
    body = json.loads(request.body)
    email = body['topup_email']
    amount = body['topup_amount']
    TopupWallet.topup_wallet('', email, amount)
    return render(request, "topup-complete.html", {})


@login_required
def payment_complete(request):
    body = json.loads(request.body)
    project_code = body['project_code']
    # print('project_code:', project_code)
    project_exists = Tasks.objects.filter(t_p_code=project_code).exists()

    try:
        project_obj = Projects.objects.get(p_code=project_code)
        project_cost = project_obj.p_usd_cost
    except Exception as e:
        project_cost = 0

    client_names = request.user.first_name + ' ' + request.user.last_name
    admin_email = 'gathogfrank@gmail.com'
    admin_obj = CustomUser.objects.get(email=admin_email)

    # update admin wallet balance
    current_wallet_balance = float(admin_obj.c_wallet_balance)
    new_wallet_balance = current_wallet_balance + project_cost
    admin_obj.c_wallet_balance = new_wallet_balance
    admin_obj.save()

    # log the transaction
    transid = get_random_string(32, 'abcdef0123456789')
    action = PaymentTransactions(
        p_projectcode=project_code,
        p_email='gathogfrank@gmail.com',
        p_transid=transid,
        c_usd_amount=project_cost,
        c_moving_balance=new_wallet_balance,
        p_direction='in',
        p_narration='Project payment from ' + client_names
    )
    action.save()

    if project_exists:
        Projects.objects.filter(p_code=project_code).update(p_status='clientsubmitted')
        Tasks.objects.filter(t_p_code=project_code).update(t_status='clientsubmitted')
    return render(request, "payment-complete.html", {})


@login_required
def checkout_page(request, project_code):
    try:
        project_obj = Projects.objects.get(p_code=project_code)
        project_title = project_obj.p_title
        project_code = project_obj.p_code
        project_cost = project_obj.p_usd_cost
    except Projects.DoesNotExist as e:
        project_title = "Project not found!"
    return render(request, "checkout.html", context={"project_title": project_title, "project_cost": project_cost,
                                                     "page_title": "Checkout", "project_code": project_code})


@login_required
def page_admin_config(request):
    try:
        configs_exists = Configs.objects.filter(~Q(buffer_in_hours=''), ~Q(words_per_hour='')).exists()

        if configs_exists:
            configs_qs = Configs.objects.filter(~Q(buffer_in_hours=''), ~Q(words_per_hour='')).first()
            buffer_in_hours = configs_qs.buffer_in_hours
            words_per_hour = configs_qs.words_per_hour
            signup_article_title = configs_qs.signup_article_title
        else:
            buffer_in_hours = ''
            words_per_hour = ''
            signup_article_title = ''

        costs = Costs.objects.values().order_by('c_id')
    except Exception as e:
        buffer_in_hours = ''
        words_per_hour = ''
        costs = ''
        print(str(e))
    return render(request, "admin-config.html", context={
        "costs": costs,
        "buffer_in_hours": buffer_in_hours,
        "words_per_hour": words_per_hour,
        "signup_article_title": signup_article_title,
        "page_title": "System Configuration"})


def view_admin_reavail_task(request):
    task_code = request.POST.get("task_code")
    response = AdminRevailTask.admin_reavail_task('', task_code)
    return HttpResponse(response, content_type='text/json')


def view_save_email_template(request):
    category_id = request.POST.get("category_id")
    email_body = request.POST.get("email_body")

    response = SaveEmailTemplate.save_email_template('', category_id, email_body)
    return HttpResponse(response, content_type='text/json')


@login_required
def email_template(request, category):
    try:
        email_template_obj = EmailTemplates.objects.get(e_cid=category)
        email_category = email_template_obj.e_category
        email_body = email_template_obj.e_mail
    except EmailTemplates.DoesNotExist:
        email_category = ''
        email_body = ''

    if category == '1':
        page_title = 'Writer Registration'
    elif category == '2':
        page_title = 'Writer Acceptance'
    elif category == '3':
        page_title = 'Writer Decline'
    elif category == '4':
        page_title = 'Client Registration'
    else:
        page_title = 'Email Template'
    return render(request, "email-template.html", context={
        "email_category_id": category,
        "email_category": email_category,
        "email_body": email_body,
        "page_title": page_title
    })


def view_verify_email(request, otp_string):
    try:
        otp_obj = CustomUser.objects.get(otp_string=otp_string)
        otp_obj.is_verified = 'yes'
        otp_obj.is_active = True
        otp_obj.otp_string = ''
        otp_obj.save()
        status = 'success'
    except Exception as e:
        status = 'fail'

    return render(request, "verify-email.html", context={
        "status": status,
        "page_title": "Email Verification"})


@login_required
def view_archived_users(request):
    archived_qs = CustomUser.objects.filter(is_archived='yes')
    return render(request, "archived-users.html", context={"archives": archived_qs, "page_title": "Archived Users"})


@login_required
def view_admins(request):
    admins_qs = CustomUser.objects.filter(userrole='2', is_archived='no')
    return render(request, "admins.html", context={"admins": admins_qs, "page_title": "Admins"})


@login_required
def view_clients(request):
    clients_qs = CustomUser.objects.filter(userrole='3', is_archived='no')
    return render(request, "clients.html", context={"clients": clients_qs, "page_title": "Clients"})


@login_required
def view_writers(request):
    writers_qs = CustomUser.objects.filter(userrole='4', is_archived='no')
    return render(request, "writers.html", context={"writers": writers_qs, "page_title": "Writers"})


@login_required
def view_add_admin(request):
    countries = list(Countries.objects.values())
    return render(request, "add-admin.html", context={"countries": countries, "page_title": "Add Admin"})


@login_required
def page_admin_profile(request, email):
    try:
        user_obj = CustomUser.objects.get(email=email)
    except Exception as e:
        user_obj = ''
    return render(request, "admin-profile.html", context={"user_details": user_obj, "page_title": "Admin Profile"})


@login_required
def page_client_profile(request, email):
    try:
        user_obj = CustomUser.objects.get(email=email)
    except Exception as e:
        user_obj = ''
    return render(request, "client-profile.html", context={"user_details": user_obj, "page_title": "Client Profile"})


@login_required
def page_writer_profile(request, email):
    try:
        user_obj = CustomUser.objects.get(email=email)
    except Exception as e:
        user_obj = ''
    return render(request, "writer-profile.html", context={"user_details": user_obj, "page_title": "Writer Profile"})


@login_required
def view_online_users(request):
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    online_users = CustomUser.objects.filter(id__in=uid_list)
    return render(request, "online-users.html", context={"online_users": online_users, "page_title": "Online Users"})


@login_required
def page_overdue_tasks(request):
    seconds_now = time.time()
    tasks_qs = Tasks.objects.filter(t_writer_deadline_secs__lte=seconds_now, t_status='writerdraft')
    return render(request, "overdue-tasks.html", context={"tasks": tasks_qs,
                                                          "page_title": "Overdue Tasks"})


@login_required
def page_topup_checkout(request):
    topup_amount = float(request.POST.get('topup-amount'))
    topup_email = str(request.POST.get('topup-email'))
    # print(topup_amount)
    return render(request, "topup-checkout.html", context={"topup_amount": topup_amount, "topup_email": topup_email,
                                                           "page_title": "Topup Wallet"})


@login_required
def topup_credit(request):
    return render(request, "topup-credit.html", context={"page_title": "Topup Wallet"})


def view_reset_password(request):
    email = request.POST.get("email")
    reset_code = request.POST.get("reset_code")
    new_password = request.POST.get("new_password")

    response = ResetPassword.reset_password('', email, reset_code, new_password)
    return HttpResponse(response, content_type='text/json')


def view_send_password_reset_code(request):
    email = request.POST.get("email")
    response = SendPasswordResetCode.send_password_reset_code('', email)
    return HttpResponse(response, content_type='text/json')


def writer_appraisal_task_page(request):
    try:
        task_obj = ApprisalTasks.objects \
            .get(t_task_code='833315adbf6a5d983f3fbbd431f5d515409eca116f516e4a6d811b7ca9ce2469')
        task_title = task_obj.t_title
    except ApprisalTasks.DoesNotExist as e:
        task_obj = ""
        task_title = "No task found!"
    categories = list(Categories.objects.values())
    return render(request, "writer-appraisal-task.html",
                  context={"categories": categories, "task": task_obj,
                           "task_title": task_title, "page_title": "Writer Appraisal Task"})


def page_pending_payments(request):
    total_owed = CustomUser.objects.filter(userrole='4').aggregate(Sum('c_wallet_balance'))['c_wallet_balance__sum']
    non_paid_tasks_qs = Tasks.objects.filter(t_status='complete', t_paid='no')
    return render(request, "pending-payments.html", context={"total_owed": total_owed, "non_paids": non_paid_tasks_qs,
                                                             "page_title": "Pending Payments"})


def messages_list_page(request):
    email = request.user.email
    messages_qs = Messages.objects.filter(m_to_email=email).order_by('-t_datetime')
    return render(request, "messages-list.html", context={"messages": messages_qs, "page_title": "Messages"})


def reset_password_page(request):
    return render(request, "reset-password.html", {})


def login_page(request):
    logout(request)
    return render(request, "login.html", {})


def add_post(request):
    return render(request, "add-post.html", {})
