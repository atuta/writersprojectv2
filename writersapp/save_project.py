from django.http import HttpResponse
import json
from .models import SystemUsers, Projects


class SaveProject:
    def __init__(self):
        pass

    def save_project(self, title, category, language, description, owner):
        try:
            action = Projects(
                p_title=title,
                p_category=category,
                p_language=language,
                p_description=description,
                p_owner=owner
            )
            action.save()
            data = {"status": "success", "data": {"message": title}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": "fail"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
