from django.http import HttpResponse
import requests
import json
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

from .models import CustomUser, EmailTemplates
from .config import EMAIL_URL


class CreateCustomUser:
    def __init__(self):
        pass

    def create_custom_user(self, firstname, lastname, phone, email, country, preferred_language, userrole, password):
        # print("email:" + email)
        email = email.strip()
        email = email.replace(' ', '')
        try:
            user_exists = CustomUser.objects.filter(email=email).exists()
            if user_exists:
                data = {"status": "fail", "data": {"message": "user_exists"}}
                return HttpResponse(json.dumps(data), content_type='text/json')

            status = False

            if userrole == '3':
                try:
                    email_template_obj = EmailTemplates.objects.get(e_cid='4')
                    email_template = email_template_obj.e_mail
                except Exception as e:
                    email_template = ''
            if userrole == '4':
                try:
                    email_template_obj = EmailTemplates.objects.get(e_cid='1')
                    email_template = email_template_obj.e_mail
                except Exception as e:
                    email_template = ''
            # print(email_template)
            otp_string = get_random_string(64, 'abcdef0123456789')
            user_id = get_random_string(96, 'abcdef0123456789')
            action = CustomUser(
                first_name=firstname,
                last_name=lastname,
                phone=phone,
                email=email,
                country=country,
                preferred_language=preferred_language,
                username=email,
                user_id=user_id,
                otp_string=otp_string,
                is_active=status,
                userrole=userrole)
            action.set_password(password)
            action.save()
            url = EMAIL_URL
            data = {'re_subject': 'Your account at ContentLancers has been created!',
                    're_message': 'Hello ' + firstname + ',<br>' + email_template,
                    're_to': email}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data=json.dumps(data), headers=headers)

            verification_data = {'re_subject': 'Email Verification!',
                                 're_message': 'Hello ' + firstname + ',<br> Kindly verify your email<br>'
                                               + '<p><a href="https://contentlancers.com/clapp/verify-email/'
                                               + otp_string + '">'
                                                              '<button type="button" '
                                                              'class="btn '
                                                              'btn-outline-primary"> '
                                                              '<i class="bi '
                                                              'bi-check-circle '
                                                              'me-1"></i>Click here to '
                                                              'verify email '
                                                              '</button></p>',
                                 're_to': email}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data=json.dumps(verification_data), headers=headers)

            data = {"status": "success", "data": {"message": firstname}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
