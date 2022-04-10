from django.http import HttpResponse
import json
from .models import SystemUsers, Projects


class SaveTask:
    def __init__(self):
        pass

    def save_task(self, title):
        try:
            data = {"status": "success", "data": {"message": title}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": "fail"}}
            return HttpResponse(json.dumps(data), content_type='text/json')

