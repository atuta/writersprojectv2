from django.http import HttpResponse
import json
from .models import Tasks, Projects
from django.utils.crypto import get_random_string
from .costs import *
import decimal


class EditTask:
    def __init__(self):
        pass

    def edit_task(self, task_code, task_title, word_count, word_count_description, keywords,
                  keyword_repetition, task_instructions, doc, writer_level, extra_proofreading,
                  priority_order, favourite_writers, deadline):
        try:
            payout_perc = decimal.Decimal(get_cost('payout_perc'))

            task_usd_cost = pre_task_cost(writer_level, word_count, extra_proofreading, priority_order)
            task_obj = Tasks.objects.get(t_task_code=task_code)
            task_obj.t_task_code = task_code
            task_obj.t_title = task_title
            task_obj.t_word_count = word_count
            task_obj.t_wc_description = word_count_description
            task_obj.t_keywords = keywords
            task_obj.t_keyword_repetition = keyword_repetition
            task_obj.t_instructions = task_instructions
            task_obj.t_doc = doc
            task_obj.p_writer_level = writer_level
            task_obj.p_extra_proofreading = extra_proofreading
            task_obj.p_priority_order = priority_order
            task_obj.p_favourite_writers = favourite_writers
            task_obj.t_usd_cost = task_usd_cost
            task_obj.t_deadline = deadline
            task_obj.t_usd_payout = task_usd_cost * payout_perc
            task_obj.save()

            data = {"status": "success", "data": {"message": task_code}}
            project_code = task_obj.t_p_code
            project_usd_cost = project_cost(project_code)

            try:
                project_obj = Projects.objects.get(p_code=project_code)
                project_obj.p_usd_cost = project_usd_cost
                project_obj.save()
            except Exception as e:
                project_obj = ""

            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
