import datetime
from datetime import datetime as dt
import time
client_deadline = "2022-05-08"
client_deadline_list = client_deadline.split('-')
new_client_deadline = str(client_deadline_list[2] + '-' + client_deadline_list[1] + '-' + client_deadline_list[0])
print(new_client_deadline)
client_deadline_in_seconds = time.mktime(datetime.datetime.strptime(new_client_deadline, "%d-%m-%Y").timetuple())
print(client_deadline_in_seconds)


today = datetime.datetime.now()
date_time = today.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:", date_time)

