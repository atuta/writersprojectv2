from django.http import HttpResponse
import json
from .models import Tasks, CustomUser, Messages
from .costs import *


class SendMessage:
    def __init__(self):
        pass

    def send_message(self, from_email, to_email, subject, body):
        try:
            from_obj = CustomUser.objects.get(email=from_email)
            to_obj = CustomUser.objects.get(email=to_email)

            from_name = from_obj.first_name + " " + from_obj.last_name
            to_name = to_obj.first_name + " " + to_obj.last_name

            action = Messages(
                m_from_email=from_email,
                m_from_name=from_name,
                m_to_email=to_email,
                m_to_name=to_name,
                m_subject=subject,
                m_body=body
            )
            action.save()

            data = {"status": "success", "data": {"message": to_email}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
