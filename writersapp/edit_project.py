from django.http import HttpResponse
import json
from .models import Projects
from django.utils.crypto import get_random_string


class EditProject:
    def __init__(self):
        pass

    def edit_project(self, project_code, title, category, language, description):
        try:
            project_obj = Projects.objects.get(p_code=project_code)
            project_obj.p_title = title
            project_obj.p_category = category
            project_obj.p_language = language
            project_obj.p_description = description
            project_obj.save()
            data = {"status": "success", "data": {"message": project_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Projects.DoesNotExist as e:
            data = {"status": "fail", "data": {"message": "fail"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
