import requests
from django.http import HttpResponse
import json

from django.utils.crypto import get_random_string

from .config import EMAIL_URL
from .models import Tasks, CustomUser, Messages
from .costs import *


class SendSiteMessage:
    def __init__(self):
        pass

    def send_site_message(self, from_email, from_name, subject, body):
        try:
            m_code = get_random_string(70, 'abcdef0123456789')
            to_email = 'support@contentlancers.com'
            action = Messages(
                m_code=m_code,
                m_from_email=from_email,
                m_from_name=from_name,
                m_to_email=to_email,
                m_to_name="ContentLancers Support",
                m_subject=subject,
                m_body=body
            )
            action.save()

            url = EMAIL_URL
            data = {'re_subject': subject,
                    're_message': body + '<p><strong>' + from_name + '</strong></p>',
                    're_to': to_email}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data=json.dumps(data), headers=headers)

            data = {"status": "success", "data": {"message": to_email}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            # print(str(e))
            data = {"status": "fail", "data": {"message": str(e)}}
        return HttpResponse(json.dumps(data), content_type='text/json')
