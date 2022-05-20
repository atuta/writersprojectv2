import json
from django.http import HttpResponse
from django.core import serializers
from .models import Tasks, ActiveTasks


class MyDrafts:

    def __init__(self):
        pass

    def my_drafts_data(self, email):

        try:
            drafts_qs = ActiveTasks.objects.filter(t_status="writerdraft", t_author=email)

            drafts = []
            for tasks in drafts_qs:
                try:
                    task_obj = Tasks.objects.get(t_task_code=tasks.t_code)
                    task = {
                        "task_code": tasks.t_code,
                        "task_title": task_obj.t_title,
                        "task_instructions": task_obj.t_instructions,
                        "payout": task_obj.t_usd_payout,
                        "deadline": task_obj.t_writer_deadline,
                        "task_date": task_obj.t_datetime
                    }
                    drafts.append(task)
                except Exception as e:
                    drafts = []
            return drafts
        except Tasks.DoesNotExist as e:
            return []
