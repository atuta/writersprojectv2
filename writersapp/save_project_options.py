from django.http import HttpResponse
import json
from .models import ProjectOptions, Tasks
from django.utils.crypto import get_random_string


class SaveProjectOptions:
    def __init__(self):
        pass

    def save_project_options(self, task_code, writer_level, extra_proofreading,
                             priority_order, favourite_writers):
        try:
            Tasks.objects.filter(t_task_code=task_code)\
                .update(
                p_writer_level=writer_level,
                p_extra_proofreading=extra_proofreading,
                p_priority_order=priority_order,
                p_favourite_writers=favourite_writers
            )
            data = {"status": "success", "data": {"message": "success"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": "fail"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
