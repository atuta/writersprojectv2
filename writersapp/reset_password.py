import requests
from django.http import HttpResponse
import json

from .config import EMAIL_URL
from .models import Tasks, ActiveTasks, CustomUser
from .costs import *
from django.utils.crypto import get_random_string


class ResetPassword:
    def __init__(self):
        pass

    def reset_password(self, email, reset_code, new_password):
        try:
            user_obj = CustomUser.objects.get(email=email)
            otp = user_obj.otp_string

            if otp != reset_code:
                data = {"status": "fail", "data": {"message": "invalid_otp"}}
                return HttpResponse(json.dumps(data), content_type='text/json')

            user_obj.set_password(new_password)
            user_obj.save()

            data = {"status": "success", "data": {"message": "password_reset"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
