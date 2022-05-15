from django.db.models import Q
from django.http import HttpResponse
import json

from django.utils.dateparse import parse_date

from .models import Tasks, Configs, CustomUser, ApprisalTasks
from django.utils.crypto import get_random_string
from .costs import *
import datetime
import time


class SaveAppraisalTask:
    def __init__(self):
        pass

    def save_appraisal_task(self, task_code, task_category, task_title, word_count, word_count_description, keywords,
                            keyword_repetition, task_instructions):
        try:

            task_exists = ApprisalTasks.objects.filter(t_task_code=task_code).exists()
            if task_exists:
                tasks_obj = ApprisalTasks.objects.get(t_task_code=task_code)
                tasks_obj.t_task_code = task_code
                tasks_obj.t_title = task_title
                tasks_obj.t_task_category = task_category
                tasks_obj.t_word_count = word_count
                tasks_obj.t_wc_description = word_count_description
                tasks_obj.t_keywords = keywords
                tasks_obj.t_keyword_repetition = keyword_repetition
                tasks_obj.t_instructions = task_instructions

                tasks_obj.save()
            else:
                action = ApprisalTasks(
                    t_task_code=task_code,
                    t_title=task_title,
                    t_task_category=task_category,
                    t_word_count=word_count,
                    t_wc_description=word_count_description,
                    t_keywords=keywords,
                    t_keyword_repetition=keyword_repetition,
                    t_instructions=task_instructions
                )
                action.save()
            data = {"status": "success", "data": {"message": task_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
