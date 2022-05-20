from django.http import HttpResponse
import json
from .models import Tasks, Messages
from django.utils.crypto import get_random_string
from .costs import *
import decimal


class MarkAllAsRead:
    def __init__(self):
        pass

    def mark_all_as_read(self, message_code):
        try:
            message_obj = Messages.objects.all()
            message_obj.m_read = 'yes'
            message_obj.save()

            data = {"status": "success", "data": {"message": message_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            print(str(e) + message_code)
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
