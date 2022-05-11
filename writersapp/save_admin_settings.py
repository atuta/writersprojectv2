from django.db.models import Q
from django.http import HttpResponse
import json
from .models import Projects, Configs
from django.utils.crypto import get_random_string


class SaveAdminSettings:
    def __init__(self):
        pass

    def save_admin_settings(self, words_per_hour, buffer_in_hours, signup_article_title):
        try:
            configs_exists = Configs.objects.filter(~Q(buffer_in_hours=''), ~Q(words_per_hour='')).exists()
            if configs_exists:
                configs_qs = Configs.objects.filter(~Q(buffer_in_hours=''), ~Q(words_per_hour='')).first()
                configs_qs.words_per_hour = words_per_hour
                configs_qs.buffer_in_hours = buffer_in_hours
                configs_qs.signup_article_title = signup_article_title
                configs_qs.save()
            else:
                action = Configs(
                    words_per_hour=words_per_hour,
                    buffer_in_hours=buffer_in_hours
                )
                action.save()
            data = {"status": "success", "data": {"message": words_per_hour}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
