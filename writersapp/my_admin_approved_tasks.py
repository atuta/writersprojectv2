import json
from django.http import HttpResponse
from django.core import serializers
from .models import Tasks, ActiveTasks


class MyAdminApprovedTasks:

    def __init__(self):
        pass

    def my_admin_approved_tasks(self, email):

        try:
            # return Tasks.objects.filter(t_status="adminwriterapproved", t_owner=email)
            tasks_qs = Tasks.objects.filter(t_status="adminwriterapproved", t_owner=email)

            admin_approved_tasks = []
            for tasks in tasks_qs:
                try:
                    active_tasks_obj = ActiveTasks.objects.get(t_code=tasks.t_task_code)
                    article = active_tasks_obj.t_article
                    task = {
                        "task_code": tasks.t_task_code,
                        "task_title": tasks.t_title,
                        "task_article": article,
                        "task_instructions": tasks.t_instructions,
                        "words_requested": tasks.t_word_count,
                        "article_words": len(article.split()),
                        "task_date": tasks.t_datetime
                    }
                    admin_approved_tasks.append(task)
                except Exception as e:
                    admin_approved_tasks = []
            return admin_approved_tasks
        except Tasks.DoesNotExist as e:
            return []
