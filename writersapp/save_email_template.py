from django.db.models import Q
from django.http import HttpResponse
import json
from .models import Projects, Configs, EmailTemplates
from django.utils.crypto import get_random_string


class SaveEmailTemplate:
    def __init__(self):
        pass

    def save_email_template(self, category_id, email_body):
        try:
            template_exists = EmailTemplates.objects.filter(e_cid=category_id).exists()
            if template_exists:
                template_obj = EmailTemplates.objects.get(e_cid=category_id)
                template_obj.e_mail = email_body
                template_obj.save()
            else:
                action = EmailTemplates(
                    e_cid=category_id,
                    e_mail=email_body
                )
                action.save()
            data = {"status": "success", "data": {"message": category_id}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
