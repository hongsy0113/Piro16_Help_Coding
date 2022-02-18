from threading import Timer
from group.views import get_invite_code
from .models import User, GetPoint, Alert
from group.models import Group
from datetime import datetime


class PeriodicTasksTimer():
    timer = None


PERIODIC_TASKS_TIMER = PeriodicTasksTimer()

# if PERIODIC_TASKS_TIMER.timer == None:
#        print(None)
#    else:
#        print(PERIODIC_TASKS_TIMER.timer.is_alive())


def initial_period(time):
    # 월요일 0시 0분 실행
    return 7 * 24 * 60 * 60 - (time.weekday() * 24 * 60 * 60 + time.hour * 60 * 60 + time.minute * 60 + time.second)


def periodic_tasks():
    unauthenticated_user_delete()
    group_code_change()
    old_alert_delete()
    old_point_delete()
    PERIODIC_TASKS_TIMER.timer = Timer(7 * 24 * 60 * 60, periodic_tasks)
    PERIODIC_TASKS_TIMER.timer.start()


def unauthenticated_user_delete():
    for user in User.objects.all():
        if not user.is_active:
            user.delete()


def group_code_change():
    for group in Group.objects.all():
        group.code = get_invite_code()
        group.save()


def old_alert_delete():
    for alert in Alert.objects.all():
        datetimefield = alert.time
        data = datetime(datetimefield.year, datetimefield.month, datetimefield.day,
                        datetimefield.hour, datetimefield.minute, datetimefield.second)
        second = int((datetime.now() - data).total_seconds())
        if second > 7 * 24 * 60 * 60:
            alert.delete()


def old_point_delete():
    for point in GetPoint.objects.all():
        datetimefield = point.get_date
        data = datetime(datetimefield.year, datetimefield.month, datetimefield.day,
                        datetimefield.hour, datetimefield.minute, datetimefield.second)
        second = int((datetime.now() - data).total_seconds())
        if second > 7 * 24 * 60 * 60:
            point.delete()
