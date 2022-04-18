import json
from django.http import HttpResponse
from django.core import serializers
from .models import WritersApplications


class PendingWriterApplications:

    def __init__(self):
        pass

    def pending_writer_applications(self):

        try:
            return list(WritersApplications.objects.filter(a_status='pending'))
        except WritersApplications.DoesNotExist as e:
            return []
