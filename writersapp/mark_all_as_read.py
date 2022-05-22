from django.db.models import Q
from django.http import HttpResponse
import json
from .models import Tasks, Messages
from django.utils.crypto import get_random_string
from .costs import *
import decimal


class MarkAllAsRead:
    def __init__(self):
        pass

    def mark_all_as_read(self):
        try:
            Messages.objects.all().update(m_read='yes')

            data = {"status": "success", "data": {"message": "success"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            print(data)
        return HttpResponse(json.dumps(data), content_type='text/json')
