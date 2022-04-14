from .models import Costs, Tasks, Projects, Costs


def get_cost(cost_name):
    try:
        cost_obj = Costs.objects.get(c_name=cost_name)
        return cost_obj.c_usd_cost
    except Costs.DoesNotExist as e:
        return ""


def task_cost(task_code):
    # get writer level
    try:
        task_obj = Tasks.objects.get(t_task_code=task_code)
        writer_level = task_obj.p_writer_level
        level_cost = get_cost(writer_level)

        # get extra proof reading
        extra_proofreading_value = task_obj.p_extra_proofreading
        if extra_proofreading_value == 'yes':
            extra_proofreading = get_cost('extra_proofreading')
        else:
            extra_proofreading = 0

        # get priority order
        priority_order_value = task_obj.p_priority_order
        if priority_order_value == 'yes':
            priority_order = get_cost('priority_order')
        else:
            priority_order = 0

        return level_cost + extra_proofreading + priority_order

    except Tasks.DoesNotExist as e:
        return 0


def project_cost(project_code):
    tasks_qs = Tasks.objects.filter(t_p_code=project_code)
    for task in tasks_qs:
        project_total_cost = 0
        project_total_cost += task_cost(task.fields.t_task_code)
    return project_total_cost
