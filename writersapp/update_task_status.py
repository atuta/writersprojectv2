from django.http import HttpResponse
import json
from .models import Tasks
from django.utils.crypto import get_random_string
from .costs import *
import decimal


class UpdateTaskStatus:
    def __init__(self):
        pass

    def update_task_status(self, task_code, task_status):
        try:
            task_obj = Tasks.objects.get(t_task_code=task_code)
            task_obj.t_status = task_status
            task_obj.save()

            data = {"status": "success", "data": {"message": task_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
