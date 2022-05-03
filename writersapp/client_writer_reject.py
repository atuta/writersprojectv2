from django.http import HttpResponse
import json
from .models import Tasks, Projects, ActiveTasks
from django.utils.crypto import get_random_string
from .costs import *
import decimal
from .init_task import InitTask


class ClientWriterReject:
    def __init__(self):
        pass

    def client_writer_reject(self, task_code):
        try:
            active_task_exists = ActiveTasks.objects.filter(t_code=task_code).exists()
            if active_task_exists:
                Tasks.objects.filter(t_task_code=task_code).update(t_status='clientwriterrejected')
                ActiveTasks.objects.filter(t_code=task_code).update(t_status='clientwriterrejected')
                data = {"status": "success", "data": {"message": task_code}}
                return HttpResponse(json.dumps(data), content_type='text/json')
            else:
                data = {"status": "fail", "data": {"message": "no_task"}}
                return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            # print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
