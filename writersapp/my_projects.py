import json
from django.http import HttpResponse
from django.core import serializers
from .models import Projects


class MyProjects:

    def __init__(self):
        pass

    def my_projects_data(self, username):

        try:
            projects_qs = Projects.objects.filter(p_owner=username)
            projects_qs_json = serializers.serialize('json', projects_qs)
            return {"status": "success", "data": json.loads(projects_qs_json)}
        except Projects.DoesNotExist as e:
            return {"status": "fail", "data": {"message": "no_data"}}
