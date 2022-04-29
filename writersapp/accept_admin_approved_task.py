from django.http import HttpResponse
import json
from .models import Tasks, ActiveTasks, CustomUser, PaymentTransactions, Projects
from .costs import *
from django.utils.crypto import get_random_string


class AcceptAdminApprovedTask:
    def __init__(self):
        pass

    def make_int(value):
        try:
            return int(value)
        except:
            return 0

    def accept_admin_approved_task(self, task_code, stars):
        try:
            Tasks.objects.filter(t_task_code=task_code).update(t_status='complete', t_stars=stars)
            ActiveTasks.objects.filter(t_code=task_code).update(t_status='complete')

            task_obj = Tasks.objects.get(t_task_code=task_code)
            email = task_obj.t_allocated_to
            payout = float(task_obj.t_usd_payout)
            users_obj = CustomUser.objects.get(email=email)
            current_stars = AcceptAdminApprovedTask.make_int(users_obj.rating_stars)
            users_obj.rating_stars = current_stars + AcceptAdminApprovedTask.make_int(stars)

            # update wallet balance
            current_wallet_balance = float(users_obj.c_wallet_balance)
            new_wallet_balance = current_wallet_balance + payout
            users_obj.c_wallet_balance = new_wallet_balance

            users_obj.save()

            # update mother project status
            project_code = task_obj.t_p_code
            tasks_qs = Tasks.objects.filter(t_p_code=project_code)

            project_status = 'complete'
            for task in tasks_qs:
                task_status = task.t_status
                if task_status != 'complete':
                    project_status = 'pending'

            project_obj = Projects.objects.get(p_code=project_code)
            project_obj.p_status = project_status
            project_obj.save()

            # log the transaction
            transid = get_random_string(32, 'abcdef0123456789')
            action = PaymentTransactions(
                p_taskcode=task_code,
                p_email=email,
                p_transid=transid,
                c_usd_amount=payout,
                c_moving_balance=new_wallet_balance,
                p_direction='in',
                p_narration='Payment for task'
            )
            action.save()

            data = {"status": "success", "data": {"message": task_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
