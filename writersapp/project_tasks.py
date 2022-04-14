import json
from django.http import HttpResponse
from django.core import serializers
from .models import Projects, Tasks


class ProjectTasks:

    def __init__(self):
        pass

    def project_tasks_data(self, project_code):

        try:
            tasks_qs = Tasks.objects.filter(t_p_code=project_code)
            tasks_qs_json = serializers.serialize('json', tasks_qs)
            return {"status": "success", "data": json.loads(tasks_qs_json)}
        except Tasks.DoesNotExist as e:
            return {"status": "fail", "data": {"message": "no_data"}}
