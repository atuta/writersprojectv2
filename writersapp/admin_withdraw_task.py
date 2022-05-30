from django.http import HttpResponse
import json
from .models import Tasks, Projects
from django.utils.crypto import get_random_string
from .costs import *
import decimal


class AdminWithdrawTask:
    def __init__(self):
        pass

    def admin_withdraw_task(self, task_code):
        try:
            task_exists = Tasks.objects.filter(t_task_code=task_code).exists()
            if task_exists:
                Tasks.objects.filter(t_task_code=task_code).update(t_status='clientsubmitted')

                data = {"status": "success", "data": {"message": task_code}}
                return HttpResponse(json.dumps(data), content_type='text/json')
            else:
                data = {"status": "fail", "data": {"message": "no_task"}}
                return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
