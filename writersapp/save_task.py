from django.http import HttpResponse
import json
from .models import Tasks
from django.utils.crypto import get_random_string
from .costs import *


class SaveTask:
    def __init__(self):
        pass

    def save_task(self, project_code, task_owner, task_title, word_count, word_count_description, keywords,
                  keyword_repetition, task_instructions, doc, writer_level, extra_proofreading,
                             priority_order, favourite_writers):
        try:
            payout_perc = decimal.Decimal(get_cost('payout_perc'))
            task_code = get_random_string(64, 'abcdef0123456789')
            task_usd_cost = pre_task_cost(writer_level, word_count, extra_proofreading, priority_order)
            action = Tasks(
                t_p_code=project_code,
                t_task_code=task_code,
                t_title=task_title,
                t_word_count=word_count,
                t_wc_description=word_count_description,
                t_keywords=keywords,
                t_keyword_repetition=keyword_repetition,
                t_instructions=task_instructions,
                t_doc=doc,
                p_writer_level=writer_level,
                p_extra_proofreading=extra_proofreading,
                p_priority_order=priority_order,
                p_favourite_writers=favourite_writers,
                t_owner=task_owner,
                t_usd_cost=task_usd_cost,
                t_usd_payout=task_usd_cost * payout_perc
            )
            action.save()
            data = {"status": "success", "data": {"message": task_code}}
            project_usd_cost = project_cost(project_code)

            try:
                project_obj = Projects.objects.get(p_code=project_code)
                project_obj.p_usd_cost = project_usd_cost
                project_obj.save()
            except Exception as e:
                project_obj = ""

            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": "fail"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
