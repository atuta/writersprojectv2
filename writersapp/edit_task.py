from django.http import HttpResponse
import json
from .models import Tasks
from django.utils.crypto import get_random_string


class EditTask:
    def __init__(self):
        pass

    def edit_task(self, task_code, task_title, word_count, word_count_description, keywords,
                  keyword_repetition, task_instructions, doc, writer_level, extra_proofreading,
                  priority_order, favourite_writers):
        try:
            task_obj = Tasks.objects.get(t_task_code=task_code)
            task_obj.t_task_code = task_code
            task_obj.t_title = task_title
            task_obj.t_word_count = word_count
            task_obj.t_wc_description = word_count_description
            task_obj.t_keywords = keywords
            task_obj.t_keyword_repetition = keyword_repetition
            task_obj.t_instructions = task_instructions
            task_obj.t_doc = doc
            task_obj.p_writer_level = writer_level
            task_obj.p_extra_proofreading = extra_proofreading
            task_obj.p_priority_order = priority_order
            task_obj.p_favourite_writers = favourite_writers
            task_obj.save()
            data = {"status": "success", "data": {"message": task_code}}
            return HttpResponse(json.dumps(data), content_type='text/json')
        except Tasks.DoesNotExist as e:
            data = {"status": "fail", "data": {"message": task_code}}
        return HttpResponse(json.dumps(data), content_type='text/json')
