from django.http import HttpResponse
import json
from .models import Tasks
from django.utils.crypto import get_random_string


class SaveTask:
    def __init__(self):
        pass

    def save_task(self, project_code, task_title, word_count, word_count_description, keywords,
                  keyword_repetition, task_instructions):
        try:
            action = Tasks(
                t_p_code=project_code,
                t_title=task_title,
                t_word_count=word_count,
                t_wc_description=word_count_description,
                t_keywords=keywords,
                t_keyword_repetition=keyword_repetition,
                t_instructions=task_instructions
            )
            action.save()
            data = {"status": "success", "data": {"message": task_title}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": "fail"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
