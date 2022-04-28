from django.http import HttpResponse
import json
from .models import Tasks
from .costs import *


class AssignTask:
    def __init__(self):
        pass

    def assign_task(self, task_code, writer_email):
        try:
            Tasks.objects.filter(t_task_code=task_code).update(t_status='adminassigned', t_allocated_to=writer_email)
            data = {"status": "success", "data": {"message": task_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
