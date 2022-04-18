from django.http import HttpResponse
import requests
import json
from django.contrib.auth.hashers import make_password
from .models import CustomUser, WritersApplications
from .config import EMAIL_URL


class SaveWriterApplication:
    def __init__(self):
        pass

    def save_writer_application(self, email, article, language):

        try:
            application_exists = WritersApplications.objects.filter(a_email=email, a_status='pending').exists()
            if application_exists:
                data = {"status": "fail", "data": {"message": "application_exists"}}
                return HttpResponse(json.dumps(data), content_type='text/json')

            try:
                user_obj = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist as e:
                user_obj = ''
            action = WritersApplications(
                a_email=email,
                a_article=article,
                a_country=user_obj.country,
                a_first_name=user_obj.first_name,
                a_last_name=user_obj.last_name,
                a_language=language)
            action.save()
            data = {"status": "success", "data": {"message": email}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
