# from django.conf import settings
# from django.core.mail import send_mail
# from django.core.mail import EmailMessage
#
# settings.configure()
#
#
# def SendEmail():
#     status = False
#     try:
#         email = EmailMessage("test", "test", to=['isaacatuta@gmail.com'])
#         email.send()
#         status = True
#     except Exception as e:
#         print(e)
#     return status
#
#
# SendEmail()
import time

from django.http import HttpResponse
import datetime

# print(datetime.datetime.now().strftime("%d-%m-%Y | %H:%M:%S"))
print(time.time())
