import json

from django.db.models import Q
from django.http import HttpResponse
from django.core import serializers
from .models import Tasks, ActiveTasks


class MyRevisions:

    def __init__(self):
        pass

    def my_revisions_data(self, email):

        try:
            revisions_qs = ActiveTasks.objects.filter(Q(t_status='adminwriterreturned') |
                                                      Q(t_status='clientwriterreturned'), t_author=email)

            revisions = []
            for tasks in revisions_qs:
                try:
                    task_obj = Tasks.objects.get(t_task_code=tasks.t_code)
                    task = {
                        "task_code": tasks.t_code,
                        "task_title": task_obj.t_title,
                        "task_instructions": task_obj.t_instructions,
                        "payout": task_obj.t_usd_payout,
                        "task_date": task_obj.t_datetime
                    }
                    revisions.append(task)
                except Exception as e:
                    revisions = []
            return revisions
        except Tasks.DoesNotExist as e:
            return []
