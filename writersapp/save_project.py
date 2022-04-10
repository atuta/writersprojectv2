from django.http import HttpResponse
import json
from .models import Projects
from django.utils.crypto import get_random_string


class SaveProject:
    def __init__(self):
        pass

    def save_project(self, title, category, language, description, owner):
        try:
            project_code = get_random_string(64, 'abcdef0123456789')
            action = Projects(
                p_title=title,
                p_category=category,
                p_language=language,
                p_description=description,
                p_code=project_code,
                p_owner=owner
            )
            action.save()
            data = {"status": "success", "data": {"message": project_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": "fail"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
