import dateutil.parser
from django.http import HttpResponse
import json

from .init_task import InitTask
from .models import Tasks, CustomUser, ActiveTasks
from .costs import *


class AssignTask:
    def __init__(self):
        pass

    def assign_task(self, task_code, user_id, admin_payout, deadline):
        try:
            user_obj = CustomUser.objects.get(user_id=user_id)
            writer_email = user_obj.email
            usernames = user_obj.first_name + " " + user_obj.last_name

            if deadline is not None:
                deadline_secs = dateutil.parser.parse(deadline, dayfirst=False).timestamp()
                Tasks.objects.filter(t_task_code=task_code).update(t_status='writerdraft',
                                                                   t_allocated_to=writer_email,
                                                                   t_allocated_to_names=usernames,
                                                                   t_usd_payout=admin_payout,
                                                                   t_writer_deadline=deadline + ':00',
                                                                   t_writer_deadline_secs=deadline_secs)
            else:
                Tasks.objects.filter(t_task_code=task_code).update(t_status='writerdraft',
                                                                   t_allocated_to=writer_email,
                                                                   t_allocated_to_names=usernames,
                                                                   t_usd_payout=admin_payout)

            # update mother project status to pending
            task_obj = Tasks.objects.get(t_task_code=task_code)
            project_code = task_obj.t_p_code
            Projects.objects.filter(p_code=project_code).update(p_status='pending')

            # delete any such task if it exists
            ActiveTasks.objects.filter(t_code=task_code).delete()

            # initialize a new active task
            InitTask.init_task('', task_code, writer_email)

            data = {"status": "success", "data": {"message": task_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
