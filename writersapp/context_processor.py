import datetime

from .models import Messages


def extras(request):
    if request.user.is_authenticated:
        email = request.user.email
        # messages
        messages_qs = Messages.objects.filter(m_to_email=email).order_by('-t_datetime')
        three_messages_qs = Messages.objects.filter(m_to_email=email).order_by('-t_datetime')[0:2]
        three_unread_qs = Messages.objects.filter(m_to_email=email, m_read='no').order_by('-t_datetime')[0:2]
        all_unread_qs = Messages.objects.filter(m_to_email=email, m_read='no').order_by('-t_datetime')
        messages_count = messages_qs.count()
        unread_count = all_unread_qs.count()
        server_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return {"server_time": server_time, "messages_count": messages_count, "three_messages": three_messages_qs,
                "three_unread": three_unread_qs, "unread_count": unread_count, "messages": messages_qs}
    else:
        return {"messages_count": "", "three_messages": "",
                "three_unread": "", "unread_count": "", "messages": ""}
