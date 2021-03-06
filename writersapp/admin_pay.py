from django.http import HttpResponse
import json
from .models import Tasks, ActiveTasks, CustomUser, PaymentTransactions, Projects
from .costs import *
from django.utils.crypto import get_random_string


class AdminPay:
    def __init__(self):
        pass

    def make_int(value):
        try:
            return int(value)
        except:
            return 0

    def admin_pay(self, task_code):
        try:
            Tasks.objects.filter(t_task_code=task_code).update(t_paid='yes')

            task_obj = Tasks.objects.get(t_task_code=task_code)
            email = task_obj.t_allocated_to
            payout = float(task_obj.t_usd_payout)
            users_obj = CustomUser.objects.get(email=email)
            writer_names = users_obj.first_name + ' ' + users_obj.last_name

            # update wallet balance
            current_wallet_balance = float(users_obj.c_wallet_balance)
            new_wallet_balance = current_wallet_balance - payout
            users_obj.c_wallet_balance = new_wallet_balance

            users_obj.save()

            # log the transaction
            transid = get_random_string(32, 'abcdef0123456789')
            action = PaymentTransactions(
                p_taskcode=task_code,
                p_email=email,
                p_transid=transid,
                c_usd_amount=payout,
                c_moving_balance=new_wallet_balance,
                p_direction='out',
                p_narration='Payment Sent'
            )
            action.save()

            # log admin transaction
            admin_email = 'gathogfrank@gmail.com'
            admin_obj = CustomUser.objects.get(email=admin_email)

            # update admin wallet balance
            current_admin_wallet_balance = float(admin_obj.c_wallet_balance)
            new_admin_wallet_balance = float(current_admin_wallet_balance) - float(payout)
            admin_obj.c_wallet_balance = new_admin_wallet_balance
            admin_obj.save()

            # log admin transaction
            admin_action = PaymentTransactions(
                p_taskcode=task_code,
                p_email=admin_email,
                p_transid=transid,
                c_usd_amount=float(payout),
                c_moving_balance=new_admin_wallet_balance,
                p_direction='out',
                p_narration='Payment for task to ' + writer_names
            )
            admin_action.save()

            data = {"status": "success", "data": {"message": task_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
