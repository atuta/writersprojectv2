from django.http import HttpResponse
import json
from .models import Tasks, Projects
from django.utils.crypto import get_random_string
from .costs import *
import decimal


class SubmitProject:
    def __init__(self):
        pass

    def submit_project(self, project_code):
        try:
            """
            project_obj = Projects.objects.get(p_code=project_code)
            project_obj.p_status = 'clientsubmitted'
            project_obj.save()
            """

            task_exists = Tasks.objects.filter(t_p_code=project_code).exists()
            if task_exists:
                Projects.objects.filter(p_code=project_code).update(p_status='clientsubmitted')
                Tasks.objects.filter(t_p_code=project_code).update(t_status='clientsubmitted')

                data = {"status": "success", "data": {"message": project_code}}
                return HttpResponse(json.dumps(data), content_type='text/json')
            else:
                data = {"status": "fail", "data": {"message": "no_task"}}
                return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
