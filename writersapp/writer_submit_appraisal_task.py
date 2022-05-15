import time
from datetime import datetime

from django.http import HttpResponse
import json
from .models import Tasks, Projects, ActiveTasks, ApprisalTasks, WritersApplications, CustomUser
from django.utils.crypto import get_random_string
from .costs import *
import decimal
from .init_task import InitTask


class WriterSubmitAppraisalTask:
    def __init__(self):
        pass

    def writer_submit_appraisal_task(self, first_name, last_name, email, article, article_words, language, country):
        task_code = '833315adbf6a5d983f3fbbd431f5d515409eca116f516e4a6d811b7ca9ce2469'
        try:
            try:
                application_exists = WritersApplications.objects.filter(a_email=email).exists()
            except Exception as e:
                application_exists = False

            if application_exists:
                data = {"status": "fail", "data": {"message": "application_exists"}}
                return HttpResponse(json.dumps(data), content_type='text/json')

            tasks_obj = ApprisalTasks.objects.get(t_task_code=task_code)
            wording_description = tasks_obj.t_wc_description
            task_words = float(tasks_obj.t_word_count)

            if wording_description == 'max':
                if float(article_words) > float(task_words):
                    data = {"status": "fail", "data": {"message": "too_many_words"}}
                    return HttpResponse(json.dumps(data), content_type='text/json')

            if wording_description == 'min':
                if float(article_words) < float(task_words):
                    data = {"status": "fail", "data": {"message": "too_few_words"}}
                    return HttpResponse(json.dumps(data), content_type='text/json')

            if wording_description == 'max':
                if float(article_words) > float(task_words):
                    data = {"status": "fail", "data": {"message": "too_many_words"}}
                    return HttpResponse(json.dumps(data), content_type='text/json')

            if wording_description == 'plus_minus_10_perc':
                required_min = float(task_words) * 0.9
                required_max = float(task_words) * 1.1

                if float(article_words) < float(required_min):
                    data = {"status": "fail", "data": {"message": "too_few_words"}}
                    return HttpResponse(json.dumps(data), content_type='text/json')

                if float(article_words) > float(required_max):
                    data = {"status": "fail", "data": {"message": "too_many_words"}}
                    return HttpResponse(json.dumps(data), content_type='text/json')

            action = WritersApplications(
                a_first_name=first_name,
                a_last_name=last_name,
                a_email=email,
                a_article=article,
                a_word_count=article_words,
                a_language=language,
                a_country=country
            )
            action.save()

            user_obj = CustomUser.objects.get(email=email)
            user_obj.writer_article = 'pending'
            user_obj.save()

            data = {"status": "success", "data": {"message": "success"}}
            return HttpResponse(json.dumps(data), content_type='text/json')

        except Exception as e:
            # print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
