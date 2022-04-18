import requests
from django.http import HttpResponse
import json

from .config import EMAIL_URL
from .models import WritersApplications, CustomUser
from django.utils.crypto import get_random_string
from .costs import *
import decimal


class RejectApplication:
    def __init__(self):
        pass

    def reject_application(self, application_id):
        try:
            application_obj = WritersApplications.objects.get(a_id=application_id)
            application_obj.a_status = 'adminrejected'
            application_obj.save()

            email = application_obj.a_email

            url = EMAIL_URL
            data = {'re_subject': 'Your application was rejected!',
                    're_message': 'Hello ' + application_obj.a_first_name + ',<br>'
                                                         '<p><h2>We are sorry that your application did not meet our '
                                                                            'minimum set requirements</h2> '
                                                         '<br>Try again next time!'
                                                         '</p>',
                    're_to': email}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data=json.dumps(data), headers=headers)

            data = {"status": "success", "data": {"message": "success"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
