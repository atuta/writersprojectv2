from django.http import HttpResponse
import json
from .models import Tasks, Projects, ActiveTasks, CustomUser, MissedDeadlines
from django.utils.crypto import get_random_string
from .costs import *
import decimal
from .init_task import InitTask


class AdminRevailTask:
    def __init__(self):
        pass

    def admin_reavail_task(self, task_code):
        try:
            task_exists = Tasks.objects.filter(t_task_code=task_code).exists()
            if task_exists:
                task_obj = Tasks.objects.get(t_task_code=task_code)

                action = MissedDeadlines(
                    t_p_code=task_obj.t_p_code,
                    t_task_code=task_obj.t_task_code,
                    t_title=task_obj.t_title,
                    t_project_category=task_obj.t_project_category,
                    t_word_count=task_obj.t_word_count,
                    t_wc_description=task_obj.t_wc_description,
                    t_keywords=task_obj.t_keywords,
                    t_keyword_repetition=task_obj.t_keyword_repetition,
                    t_instructions=task_obj.t_instructions,
                    t_doc=task_obj.t_doc,
                    p_writer_level=task_obj.p_writer_level,
                    p_extra_proofreading=task_obj.p_extra_proofreading,
                    p_priority_order=task_obj.p_priority_order,
                    t_urgent=task_obj.t_urgent,
                    p_favourite_writers=task_obj.p_favourite_writers,
                    t_owner=task_obj.t_owner,
                    t_owner_names=task_obj.t_owner_names,
                    t_usd_cost=task_obj.t_usd_cost,
                    t_deadline=task_obj.t_deadline,
                    t_writer_deadline=task_obj.t_writer_deadline,
                    t_writer_deadline_secs=task_obj.t_writer_deadline_secs,
                    t_usd_payout=task_obj.t_usd_payout
                )
                action.save()

                ActiveTasks.objects.filter(t_code=task_code).update(t_status='terminated', t_code='', t_author='')
                Tasks.objects.filter(t_task_code=task_code).update(t_status='adminsubmitted')
                Projects.objects.filter(p_code=task_obj.t_p_code).update(p_status='adminsubmitted')

                allocated_to = task_obj.t_allocated_to
                blacklisted_emails = task_obj.t_blacklisted_emails
                new_blacklisted_emails = blacklisted_emails + ',' + allocated_to

                user_obj = CustomUser.objects.get(email=allocated_to)
                stars = user_obj.rating_stars
                new_stars = float(stars) - 5
                user_obj.rating_stars = new_stars
                user_obj.save()

                task_obj.t_blacklisted_emails = new_blacklisted_emails
                task_obj.t_status = 'adminsubmitted'
                task_obj.t_allocated_to = ''
                task_obj.save()

                data = {"status": "success", "data": {"message": task_code}}
                return HttpResponse(json.dumps(data), content_type='text/json')
            else:
                data = {"status": "fail", "data": {"message": "no_task"}}
                return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            # print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
