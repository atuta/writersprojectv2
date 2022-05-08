from django.http import HttpResponse
import requests
import json
from django.contrib.auth.hashers import make_password
from .models import CustomUser, WritersApplications
from .config import EMAIL_URL


class SaveWriterApplication:
    def __init__(self):
        pass

    def save_writer_application(self, email, article, country, first_name, last_name, language):
        action = WritersApplications(
            a_email=email,
            a_article=article,
            a_country=country,
            a_first_name=first_name,
            a_last_name=last_name,
            a_language=language)
        action.save()
