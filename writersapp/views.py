import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .create_account import CreateSystemUser
from .login import CustomLogin
from .models import Categories


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

