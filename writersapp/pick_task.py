from django.http import HttpResponse
import json
from .models import Tasks, Projects
from django.utils.crypto import get_random_string
from .costs import *
import decimal
from .init_task import InitTask


class PickTask:
    def __init__(self):
        pass

    def pick_task(self, task_code, email):
        try:
            task_exists = Tasks.objects.filter(t_task_code=task_code, t_status='clientsubmitted').exists()
            if task_exists:

                # update mother project status to pending
                task_obj = Tasks.objects.get(t_task_code=task_code)
                project_code = task_obj.t_p_code
                Projects.objects.filter(p_code=project_code).update(p_status='pending')

                Tasks.objects.filter(t_task_code=task_code).update(t_status='writerdraft', t_allocated_to=email)
                InitTask.init_task('', task_code, email)
                data = {"status": "success", "data": {"message": task_code}}
                return HttpResponse(json.dumps(data), content_type='text/json')
            else:
                data = {"status": "fail", "data": {"message": "no_task"}}
                return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            # print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
