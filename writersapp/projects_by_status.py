import json
from django.http import HttpResponse
from django.core import serializers
from .models import WritersApplications


class ProjectsByStatus:

    def __init__(self):
        pass

    def projects_by_status(self, status):

        try:
            projects_qs = WritersApplications.objects.filter(p_status=status)
            projects_qs_json = serializers.serialize('json', projects_qs)
            return {"status": "success", "data": json.loads(projects_qs_json)}
        except WritersApplications.DoesNotExist as e:
            return {"status": "fail", "data": {"message": "no_data"}}
