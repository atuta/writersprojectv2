from django.db.models import Q
from django.http import HttpResponse
import json

from django.utils.dateparse import parse_date

from .models import Tasks, Configs, CustomUser
from django.utils.crypto import get_random_string
from .costs import *
import datetime
import time


class SaveTask:
    def __init__(self):
        pass

    def save_task(self, project_code, task_owner, task_title, word_count, word_count_description, keywords,
                  keyword_repetition, task_instructions, doc, writer_level, extra_proofreading,
                  priority_order, favourite_writers, deadline):
        try:

            try:
                configs_exists = Configs.objects.filter(~Q(buffer_in_hours=''), ~Q(words_per_hour='')).exists()

                if configs_exists:
                    configs_qs = Configs.objects.filter(~Q(buffer_in_hours=''), ~Q(words_per_hour='')).first()
                    buffer_in_hours = configs_qs.buffer_in_hours
                    words_per_hour = configs_qs.words_per_hour
                else:
                    buffer_in_hours = ''
                    words_per_hour = ''
            except Exception as e:
                buffer_in_hours = ''
                words_per_hour = ''

            task_hours = float(word_count) / float(words_per_hour)
            task_seconds = float(task_hours) * 60 * 60
            buffer_seconds = float(buffer_in_hours) * 60 * 60
            current_seconds = datetime.datetime.now().timestamp()

            # if the client has not provided deadline system gives a deadline of 2 days
            if deadline == '':
                deadline = str(datetime.date.today() + datetime.timedelta(days=2))

            client_deadline_list = deadline.split('-')
            new_client_deadline = str(
                client_deadline_list[2] + '-' + client_deadline_list[1] + '-' + client_deadline_list[0])

            client_deadline_in_seconds = time.mktime(
                datetime.datetime.strptime(new_client_deadline, "%d-%m-%Y").timetuple())

            admin_deadline_seconds = float(client_deadline_in_seconds) - buffer_seconds
            natural_deadline_seconds = float(current_seconds) + task_seconds

            if natural_deadline_seconds > admin_deadline_seconds:
                data = {"status": "fail", "data": {"message": "deadline_too_close"}}
                return HttpResponse(json.dumps(data), content_type='text/json')
            else:
                writer_deadline = datetime.datetime.fromtimestamp(float(admin_deadline_seconds))

            payout_perc = decimal.Decimal(get_cost('payout_perc'))
            task_code = get_random_string(64, 'abcdef0123456789')
            task_usd_cost = pre_task_cost(writer_level, word_count, extra_proofreading, priority_order)

            task_owner_obj = CustomUser.objects.get(email=task_owner)
            task_owner_names = task_owner_obj.first_name + ' ' + task_owner_obj.last_name
            initial_project_obj = Projects.objects.get(p_code=project_code)
            project_category = initial_project_obj.p_category
            action = Tasks(
                t_p_code=project_code,
                t_task_code=task_code,
                t_title=task_title,
                t_project_category=project_category,
                t_word_count=word_count,
                t_wc_description=word_count_description,
                t_keywords=keywords,
                t_keyword_repetition=keyword_repetition,
                t_instructions=task_instructions,
                t_doc=doc,
                p_writer_level=writer_level,
                p_extra_proofreading=extra_proofreading,
                p_priority_order=priority_order,
                t_urgent=priority_order,
                p_favourite_writers=favourite_writers,
                t_owner=task_owner,
                t_owner_names=task_owner_names,
                t_usd_cost=task_usd_cost,
                t_deadline=deadline,
                t_writer_deadline=writer_deadline,
                t_writer_deadline_secs=admin_deadline_seconds,
                t_usd_payout=(task_usd_cost * payout_perc)
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
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
