from django.http import HttpResponse
import requests
import json
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .config import EMAIL_URL


class CreateCustomUser:
    def __init__(self):
        pass

    def create_custom_user(self, firstname, lastname, phone, email, country, userrole, password):

        try:
            user_exists = CustomUser.objects.filter(email=email).exists()
            if user_exists:
                data = {"status": "fail", "data": {"message": "user_exists"}}
                return HttpResponse(json.dumps(data), content_type='text/json')

            action = CustomUser(
                first_name=firstname,
                last_name=lastname,
                phone=phone,
                email=email,
                country=country,
                username=email,
                userrole=userrole)
            action.set_password(password)
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
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
