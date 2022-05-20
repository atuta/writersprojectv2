from django.db.models import Q
from django.http import HttpResponse
import json
from .models import Tasks, Projects, FavoriteWriters
from django.utils.crypto import get_random_string
from .costs import *
import decimal
from .init_task import InitTask


class PickTask:
    def __init__(self):
        pass

    def pick_task(self, task_code, email):
        try:
            task_exists = Tasks.objects.filter(Q(t_status='adminwriterreturned') | Q(t_status='clientwriterreturned')
                                               | Q(t_status='clientsubmitted'),
                                               t_task_code=task_code).exists()
            if task_exists:

                # update mother project status to pending
                task_obj = Tasks.objects.get(t_task_code=task_code)
                client_email = task_obj.t_owner

                # check whether the email is blacklisted
                blacklisted = Tasks.objects.filter(t_blacklisted_emails__contains=email, t_task_code=task_code).exists()
                if blacklisted:
                    data = {"status": "fail", "data": {"message": "blacklisted"}}
                    return HttpResponse(json.dumps(data), content_type='text/json')

                favourite_writers = task_obj.p_favourite_writers
                if favourite_writers == 'yes':
                    # check if the client has favourite writers
                    has_favourite_writers = FavoriteWriters.objects.filter(f_client_email=client_email).exists()
                    if has_favourite_writers:
                        # check if the writer exists in the client's favourite list
                        writer_favourite = FavoriteWriters.objects\
                            .filter(f_client_email=client_email, f_writer_email=email).exists()
                        if not writer_favourite:
                            data = {"status": "fail", "data": {"message": "not_favourite"}}
                            return HttpResponse(json.dumps(data), content_type='text/json')

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
