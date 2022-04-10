import json
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .save_task import SaveTask
from .save_project_options import SaveProjectOptions
from .save_project import SaveProject
from .create_account import CreateSystemUser
from .login import CustomLogin
from .models import Categories


@api_view(['POST', 'GET'])
@csrf_exempt
def view_save_project_options(request):
    received_data = json.loads(request.body)
    # project_code, writer_level, extra_proofreading, priority_order, favourite_writers
    project_code = received_data['project_code']
    writer_level = received_data['writer_level']
    extra_proofreading = received_data['extra_proofreading']
    priority_order = received_data['priority_order']
    favourite_writers = received_data['favourite_writers']

    response = SaveProjectOptions.save_project_options('', project_code, writer_level, extra_proofreading,
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
def view_save_task(request):
    received_data = json.loads(request.body)

    project_code = received_data['project_code']
    task_title = received_data['task_title']
    word_count = received_data['word_count']
    word_count_description = received_data['word_count_description']
    keywords = received_data['keywords']
    keyword_repetition = received_data['keyword_repetition']
    task_instructions = received_data['task_instructions']

    response = SaveTask.save_task('', project_code, task_title, word_count, word_count_description, keywords,
                                  keyword_repetition, task_instructions)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_save_project(request):
    received_data = json.loads(request.body)

    title = received_data['title']
    category = received_data['category']
    language = received_data['language']
    description = received_data['description']
    owner = received_data['owner']

    response = SaveProject.save_project('', title, category, language, description, owner)
    return HttpResponse(response, content_type='text/json')


@api_view(['POST', 'GET'])
@csrf_exempt
def view_custom_login(request):
    received_data = json.loads(request.body)
    username = received_data['email']
    password = received_data['password']

    response = CustomLogin.custom_login('', username, password)
    return HttpResponse(response, content_type='text/json')


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


def create_project(request):
    categories = list(Categories.objects.values())
    return render(request, "project-wizard.html", context={"categories": categories})


def home(request):
    return render(request, "index.html", {})


def dashbooard(request):
    return render(request, "dashboard.html", {})


def login(request):
    return render(request, "login.html", {})


def add_post(request):
    return render(request, "add-post.html", {})
