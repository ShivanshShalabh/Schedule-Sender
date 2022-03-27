import datetime
import calendar


def findDay(date):
    date_ = datetime.datetime.strptime(date, '%d %m %Y').weekday()
    return (calendar.day_name[date_])


# Time_table
MONDAY = """
Monday's timetable
8:00 - 8:40 - Physics
8:50 - 9:30 - Physics
10:05 - 10:45 - Math
10:55 - 11:35 - Computer Science
11:45 - 12:25 - Chemistry 
12:35 - 13:15 - Chemistry

"""
TUESDAY = """
Tuesday's timetable
8:00 - 8:40 - English
8:50 - 9:30 - Chemistry 
10:05 - 10:45 - Math
10:55 - 11:35 - Physics
11:45 - 12:25 - Computer Science
12:35 - 13:15 - Computer Science
"""
WEDNESDAY = """
Wednesday's timetable
8:00 - 8:40 - Physics
8:50 - 9:30 - English
10:05 - 10:45 - Math
10:55 - 11:35 - Computer Science
11:45 - 12:25 - English
12:35 - 13:15 - Chemistry
"""
THURSDAY = """
Thursday's timetable
8:00 - 8:40 - English
8:50 - 9:30 - Math
10:05 - 10:45 - Math
10:55 - 11:35 - Chemistry 
11:45 - 12:25 - Physics
12:35 - 13:15 - Computer Science
"""
FRIDAY = """
Friday's timetable
8:00 - 8:40 - English
8:50 - 9:30 - Math
10:05 - 10:45 - Math
10:55 - 11:35 - Chemistry
11:45 - 12:25 - Physics
12:35 - 13:15 - Computer Science
"""
last_updated = "*The timetable was last updated on 17th January, 2022*"


time_table = {'Monday': MONDAY, 'Tuesday': TUESDAY,
              'Wednesday': WEDNESDAY, 'Thursday': THURSDAY, 'Friday': FRIDAY}
