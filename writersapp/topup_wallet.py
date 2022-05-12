from django.http import HttpResponse
import json
from .models import Tasks, ActiveTasks, CustomUser, PaymentTransactions, Projects
from .costs import *
from django.utils.crypto import get_random_string


class TopupWallet:
    def __init__(self):
        pass

    def make_int(value):
        try:
            return int(value)
        except:
            return 0

    def topup_wallet(self, email, amount):
        try:
            users_obj = CustomUser.objects.get(email=email)

            # update wallet balance
            current_wallet_balance = float(users_obj.c_wallet_balance)
            new_wallet_balance = current_wallet_balance + float(amount)
            users_obj.c_wallet_balance = new_wallet_balance

            users_obj.save()

            # log the transaction
            transid = get_random_string(32, 'abcdef0123456789')
            action = PaymentTransactions(
                p_taskcode=email,
                p_email=email,
                p_transid=transid,
                c_usd_amount=float(amount),
                c_moving_balance=new_wallet_balance,
                p_direction='in',
                p_narration='Wallet top up'
            )
            action.save()
            return 'success'
        except Exception as e:
            return 'fail'
