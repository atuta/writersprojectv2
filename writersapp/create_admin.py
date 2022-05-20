from django.http import HttpResponse
import requests
import json
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

from .models import CustomUser, EmailTemplates
from .config import EMAIL_URL


class CreateAdmin:
    def __init__(self):
        pass

    def create_admin(self, firstname, lastname, phone, email, country):

        try:
            user_exists = CustomUser.objects.filter(email=email).exists()
            if user_exists:
                data = {"status": "fail", "data": {"message": "user_exists"}}
                return HttpResponse(json.dumps(data), content_type='text/json')
            password = get_random_string(6, '23456789')
            action = CustomUser(
                first_name=firstname,
                last_name=lastname,
                phone=phone,
                email=email,
                country=country,
                username=email,
                is_active=True,
                is_verified='yes',
                userrole='2')
            action.set_password(password)
            action.save()
            url = EMAIL_URL

            verification_data = {'re_subject': 'Admin Account Created!',
                                 're_message': 'Hello ' + firstname + ',<br> your admin account has been created. '
                                              'Your start password is: <h1>' + password + '</h1>. '
                                                'We recommened you change it on your first login. <br> Thank you.',
                                 're_to': email}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data=json.dumps(verification_data), headers=headers)

            data = {"status": "success", "data": {"message": firstname}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
