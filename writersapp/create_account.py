from django.http import HttpResponse
import requests
import json
from django.contrib.auth.hashers import make_password
from .models import SystemUsers
from .config import EMAIL_URL


class CreateSystemUser:
    def __init__(self):
        pass

    def create_system_user(self, firstname, lastname, phone, email, country, role, password):

        try:
            user_exists = SystemUsers.objects.filter(s_email=email).exists()
            if user_exists:
                data = {"status": "fail", "data": {"message": "user_exists"}}
                return HttpResponse(json.dumps(data), content_type='text/json')

            action = SystemUsers(s_firstname=firstname,
                                 s_lastname=lastname,
                                 s_phone=phone,
                                 s_email=email,
                                 s_country=country,
                                 s_role=role,
                                 s_passwd=make_password(password))
            action.save()
            url = EMAIL_URL
            data = {'re_subject': 'Your writers account has been created!',
                    're_message': 'Hello ' + firstname + ',<br>'
                                                          '<p><h2>Welcome to the Writers Community</h2> '
                                                          '<br>Your account has been created successfully!'
                                                         '</p>',
                    're_to': email}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data=json.dumps(data), headers=headers)
            data = {"status": "success", "data": {"message": firstname}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": "fail"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
