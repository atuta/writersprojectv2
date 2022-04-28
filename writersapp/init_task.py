from django.http import HttpResponse
import json
from .models import Tasks, ActiveTasks
from .costs import *
from django.utils.crypto import get_random_string


class InitTask:
    def __init__(self):
        pass

    def init_task(self, task_code, author):
        try:
            task_obj = Tasks.objects.get(t_task_code=task_code)
            # t_writer_reward
            writer_reward = task_obj.t_usd_payout
            action = ActiveTasks(
                t_code=task_code,
                t_writer_reward=writer_reward,
                t_author=author
            )
            action.save()
        except Exception as e:
            return str(e)
