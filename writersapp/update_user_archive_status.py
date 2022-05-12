from django.http import HttpResponse
import requests
import json
from .models import CustomUser


class UpdateUserArchiveStatus:
    def __init__(self):
        pass

    def update_user_archive_status(self, email, status):
        # print(email)
        try:
            if status == 'yes':
                active = False
            else:
                status = 'no'
                active = True
            user_obj = CustomUser.objects.get(email=email)
            user_obj.is_archived = status
            user_obj.is_active = active
            user_obj.save()

            data = {"status": "success", "data": {"message": user_obj.userrole}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return HttpResponse(json.dumps(data), content_type='text/json')
