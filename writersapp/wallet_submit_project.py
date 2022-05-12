from django.http import HttpResponse
import json
from .models import Tasks, Projects, CustomUser, PaymentTransactions
from django.utils.crypto import get_random_string
from .costs import *
import decimal


class WalletSubmitProject:
    def __init__(self):
        pass

    def wallet_submit_project(self, project_code):
        try:
            project_obj = Projects.objects.get(p_code=project_code)
            email = project_obj.p_owner
            cost = project_obj.p_usd_cost
            users_obj = CustomUser.objects.get(email=email)

            # update wallet balance
            current_wallet_balance = float(users_obj.c_wallet_balance)

            if current_wallet_balance < cost:
                data = {"status": "fail", "data": {"message": "insufficient_balance"}}
                return HttpResponse(json.dumps(data), content_type='text/json')

            new_wallet_balance = current_wallet_balance - float(cost)
            users_obj.c_wallet_balance = new_wallet_balance

            users_obj.save()

            # log the transaction
            transid = get_random_string(32, 'abcdef0123456789')
            action = PaymentTransactions(
                p_projectcode=project_code,
                p_email=email,
                p_transid=transid,
                c_usd_amount=float(cost),
                c_moving_balance=new_wallet_balance,
                p_direction='out',
                p_narration='Project checkout'
            )
            action.save()

            task_exists = Tasks.objects.filter(t_p_code=project_code).exists()
            if task_exists:
                Projects.objects.filter(p_code=project_code).update(p_status='clientsubmitted')
                Tasks.objects.filter(t_p_code=project_code).update(t_status='clientsubmitted')

                data = {"status": "success", "data": {"message": project_code}}
                return HttpResponse(json.dumps(data), content_type='text/json')
            else:
                data = {"status": "fail", "data": {"message": "no_task"}}
                return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
