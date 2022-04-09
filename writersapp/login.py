import json
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

from .models import SystemUsers


class CustomLogin:

    def __init__(self):
        pass

    def custom_login(self, username_raw, password_raw):

        username = username_raw.strip()
        username = username.lower()
        password = password_raw.strip()

        try:
            account_obj = SystemUsers.objects.get(s_email=username)
            existing_password = account_obj.s_passwd

            matchcheck = check_password(password, existing_password)

            if matchcheck:
                data = {"status": "success", "data": {"message": "login_success",
                                                      "email": str(account_obj.s_email),
                                                      "phone": str(account_obj.s_phone),
                                                      "firstname": account_obj.s_firstname,
                                                      "lastname": str(account_obj.s_lastname),
                                                      "country": str(account_obj.s_country),
                                                      "role": str(account_obj.s_role)
                                                      }}
                return HttpResponse(json.dumps(data), content_type='text/json')
            else:
                data = {"status": "fail", "data": {"message": "login_failed"}}
                return HttpResponse(json.dumps(data), content_type='text/json')

        except SystemUsers.DoesNotExist as e:
            data = {"status": "fail", "data": {"message": "login_failed"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
