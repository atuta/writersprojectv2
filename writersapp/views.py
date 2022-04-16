import json

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .edit_task import EditTask
from .save_task import SaveTask
from .save_project_options import SaveProjectOptions
from .log_task import LogTask
from .edit_project import EditProject
from .save_project import SaveProject
from .project_tasks import ProjectTasks
from .my_projects import MyProjects
from .create_account import CreateSystemUser
from .login import CustomLogin
from .models import Categories, Projects, Tasks, ActiveTasks
from django.contrib.auth import authenticate, login, logout


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
def view_log_task(request):
    task_code = request.POST.get("task_code")
    article = request.POST.get("article")
    author = request.user.email

    response = LogTask.log_task('', task_code, article, author)
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

    response = EditTask.edit_task('', task_code, task_title, word_count, word_count_description, keywords,
                                  keyword_repetition, task_instructions, doc, writer_level, extra_proofreading,
                                  priority_order, favourite_writers)
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

    response = SaveTask.save_task('', project_code, task_title, word_count, word_count_description, keywords,
                                  keyword_repetition, task_instructions, doc, writer_level, extra_proofreading,
                                  priority_order, favourite_writers)
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
        data = {"status": "success", "data": {"message": "login_success"}}
        return HttpResponse(json.dumps(data), content_type='text/json')
    else:
        data = {"status": "fail", "data": {"message": "login_fail"}}
        return HttpResponse(json.dumps(data), content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_create_account(request):
    received_data = json.loads(request.body)
    firstname = received_data['firstname']
    lastname = received_data['lastname']
    phone = received_data['phone']
    email = received_data['email']
    country = received_data['country']
    role = received_data['role']
    password = received_data['password']

    response = CreateSystemUser.create_system_user('', firstname, lastname, phone, email, country, role, password)
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
    except Projects.DoesNotExist as e:
        response = {}
        project_title = "No task found!"
    return render(request, "project-tasks.html", context={"data": response, "page_title": project_title})


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


def page_my_projects(request):
    response = MyProjects.my_projects_data('', request.user.email)
    return render(request, "my-projects.html", context={"data": response, "page_title": "Available Projects"})


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


def dashbooard(request):
    return render(request, "dashboard.html", {})


def login_page(request):
    logout(request)
    return render(request, "login.html", {})


def add_post(request):
    return render(request, "add-post.html", {})
