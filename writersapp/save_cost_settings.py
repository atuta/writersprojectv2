from django.db.models import Q
from django.http import HttpResponse
import json
from .models import Projects, Configs, Costs
from django.utils.crypto import get_random_string


class SaveCostSettings:
    def __init__(self):
        pass

    def save_cost_settings(self, basic, standard, expert, extra_proofreading, priority_order, payout_perc):
        try:
            basic_obj = Costs.objects.get(c_name='basic')
            basic_obj.c_usd_cost = basic
            basic_obj.save()

            standard_obj = Costs.objects.get(c_name='standard')
            standard_obj.c_usd_cost = standard
            standard_obj.save()

            expert_obj = Costs.objects.get(c_name='expert')
            expert_obj.c_usd_cost = expert
            expert_obj.save()

            extra_proofreading_obj = Costs.objects.get(c_name='extra_proofreading')
            extra_proofreading_obj.c_usd_cost = extra_proofreading
            extra_proofreading_obj.save()

            priority_order_obj = Costs.objects.get(c_name='priority_order')
            priority_order_obj.c_usd_cost = priority_order
            priority_order_obj.save()

            payout_perc_obj = Costs.objects.get(c_name='payout_perc')
            payout_perc_obj.c_usd_cost = payout_perc
            payout_perc_obj.save()

            data = {"status": "success", "data": {"message": "success"}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
