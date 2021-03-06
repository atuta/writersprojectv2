from django.http import HttpResponse
import requests
import json
from .models import CustomUser


class UpdateUserStatus:
    def __init__(self):
        pass

    def update_user_status(self, email, status):
        print(email)
        try:
            if status == 'active':
                status = True
            else:
                status = False
            user_obj = CustomUser.objects.get(email=email)
            user_obj.is_active = status
            user_obj.save()

            data = {"status": "success", "data": {"message": email}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
