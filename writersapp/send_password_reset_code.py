import requests
from django.http import HttpResponse
import json

from .config import EMAIL_URL
from .models import Tasks, ActiveTasks, CustomUser
from .costs import *
from django.utils.crypto import get_random_string


class SendPasswordResetCode:
    def __init__(self):
        pass

    def send_password_reset_code(self, email):
        try:
            otp = get_random_string(6, '23456789')

            user_obj = CustomUser.objects.get(email=email)
            user_obj.otp_string = otp
            user_obj.save()

            url = EMAIL_URL
            data = {'re_subject': 'Password Reset Code',
                    're_message': 'Use the following code to reset your password: '
                                  '<h1>' + otp + '</h1> Thank you. <br> <strong>ContentLancers Team</strong>',
                    're_to': email}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data=json.dumps(data), headers=headers)

            data = {"status": "success", "data": {"message": "email_sent"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": "not_sent"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
