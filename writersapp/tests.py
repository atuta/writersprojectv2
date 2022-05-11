import calendar
import datetime
import time

date_example = "2022-05-10 14:00:00"
date_format = datetime.datetime.strptime(date_example,
                                         "%Y-%m-%d %H:%M:%S")
unix_time = datetime.datetime.timestamp(date_format)
print(unix_time)


