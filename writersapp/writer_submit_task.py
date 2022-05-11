import time
from datetime import datetime

from django.http import HttpResponse
import json
from .models import Tasks, Projects, ActiveTasks
from django.utils.crypto import get_random_string
from .costs import *
import decimal
from .init_task import InitTask


class WriterSubmitTask:
    def __init__(self):
        pass

    def writer_submit_task(self, task_code):
        try:
            active_task_exists = ActiveTasks.objects.filter(t_code=task_code).exists()
            if active_task_exists:
                active_tasks_obj = ActiveTasks.objects.get(t_code=task_code)
                article_words = float(active_tasks_obj.t_article_word_count)

                tasks_obj = Tasks.objects.get(t_task_code=task_code)
                wording_description = tasks_obj.t_wc_description
                task_words = float(tasks_obj.t_word_count)

                if wording_description == 'min':
                    if article_words < task_words:
                        data = {"status": "fail", "data": {"message": "too_few_words"}}
                        return HttpResponse(json.dumps(data), content_type='text/json')

                if wording_description == 'max':
                    if article_words > task_words:
                        data = {"status": "fail", "data": {"message": "too_many_words"}}
                        return HttpResponse(json.dumps(data), content_type='text/json')

                if wording_description == 'plus_minus_10_perc':
                    required_min = float(task_words) * 0.9
                    required_max = float(task_words) * 1.1

                    if article_words < required_min:
                        data = {"status": "fail", "data": {"message": "too_few_words"}}
                        return HttpResponse(json.dumps(data), content_type='text/json')

                    if article_words > required_max:
                        data = {"status": "fail", "data": {"message": "too_many_words"}}
                        return HttpResponse(json.dumps(data), content_type='text/json')

                writer_deadline = tasks_obj.t_writer_deadline
                writer_deadline_format = datetime.strptime(writer_deadline,
                                                                     "%Y-%m-%d %H:%M:%S")
                writer_deadline_seconds = datetime.timestamp(writer_deadline_format)
                now_seconds = time.time()

                if float(now_seconds) > float(writer_deadline_seconds):
                    data = {"status": "fail", "data": {"message": "past_deadline"}}
                    return HttpResponse(json.dumps(data), content_type='text/json')

                Tasks.objects.filter(t_task_code=task_code).update(t_status='writersubmitted')
                ActiveTasks.objects.filter(t_code=task_code).update(t_status='writersubmitted')
                data = {"status": "success", "data": {"message": task_code}}
                return HttpResponse(json.dumps(data), content_type='text/json')
            else:
                data = {"status": "fail", "data": {"message": "no_task"}}
                return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            # print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
