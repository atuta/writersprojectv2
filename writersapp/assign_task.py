from django.http import HttpResponse
import json

from .init_task import InitTask
from .models import Tasks, CustomUser
from .costs import *


class AssignTask:
    def __init__(self):
        pass

    def assign_task(self, task_code, user_id, admin_payout):
        try:
            user_obj = CustomUser.objects.get(user_id=user_id)
            writer_email = user_obj.email
            Tasks.objects.filter(t_task_code=task_code).update(t_status='writerdraft',
                                                               t_allocated_to=writer_email, t_usd_payout=admin_payout)

            # update mother project status to pending
            task_obj = Tasks.objects.get(t_task_code=task_code)
            project_code = task_obj.t_p_code
            Projects.objects.filter(p_code=project_code).update(p_status='pending')

            InitTask.init_task('', task_code, writer_email)

            data = {"status": "success", "data": {"message": task_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
