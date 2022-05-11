import json
from django.http import HttpResponse
from django.core import serializers
from .models import Tasks, ActiveTasks


class PendingAdminApprovals:

    def __init__(self):
        pass

    def pending_admin_approvals(self):

        try:
            drafts_qs = ActiveTasks.objects.filter(t_status="writersubmitted")

            drafts = []
            for tasks in drafts_qs:
                try:
                    task_obj = Tasks.objects.get(t_task_code=tasks.t_code)
                    article = tasks.t_article
                    task = {
                        "task_code": tasks.t_code,
                        "task_article": tasks.t_article,
                        "task_title": task_obj.t_title,
                        "task_instructions": task_obj.t_instructions,
                        "payout": task_obj.t_usd_payout,
                        "words_requested": task_obj.t_word_count,
                        "article_words": len(article.split()),
                        "client_name": task_obj.t_owner_names,
                        "task_deadline": task_obj.t_deadline,
                        "task_date": task_obj.t_datetime
                    }
                    drafts.append(task)
                except Exception as e:
                    drafts = []
            return drafts
        except Tasks.DoesNotExist as e:
            return []
