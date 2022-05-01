from django.http import HttpResponse
import json
from .models import Tasks, ActiveTasks
from .costs import *
from django.utils.crypto import get_random_string


class LogTask:
    def __init__(self):
        pass

    def log_task(self, task_code, article, author):
        try:
            # task_exists = ActiveTasks.objects.filter(t_code=task_code).exists()
            task_total_cost = task_cost(task_code)

            try:
                active_tasks_obj = ActiveTasks.objects.get(t_code=task_code)
                active_tasks_obj.t_article = article
                active_tasks_obj.save()
            except ActiveTasks.DoesNotExist as e:
                action = ActiveTasks(
                    t_code=task_code,
                    t_article=article,
                    t_writer_reward=task_total_cost,
                    t_author=author
                )
                action.save()
            data = {"status": "success", "data": {"message": task_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
