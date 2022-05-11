import requests
from django.http import HttpResponse
import json

from .config import EMAIL_URL
from .models import WritersApplications, CustomUser, EmailTemplates
from django.utils.crypto import get_random_string
from .costs import *
import decimal


class ApproveApplication:
    def __init__(self):
        pass

    def approve_application(self, application_id):
        try:
            application_obj = WritersApplications.objects.get(a_id=application_id)
            application_obj.a_status = 'adminapproved'
            application_obj.save()

            email = application_obj.a_email
            language = application_obj.a_language

            user_obj = CustomUser.objects.get(email=email)
            user_obj.preferred_language = language
            user_obj.userrole = '4'
            user_obj.is_active = True
            user_obj.save()

            try:
                email_template_obj = EmailTemplates.objects.get(e_cid='3')
                email_template = email_template_obj.e_mail
            except Exception as e:
                email_template = ''

            url = EMAIL_URL
            data = {'re_subject': 'You application has been approved!',
                    're_message': 'Hello ' + application_obj.a_first_name + ',<br>' + email_template,
                    're_to': email}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data=json.dumps(data), headers=headers)

            data = {"status": "success", "data": {"message": "success"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
