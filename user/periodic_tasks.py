from threading import Timer
from group.views import get_invite_code
from .models import User
from group.models import Group


def initial_period(time):
    # 월요일 0시 0분 실행
    return 7 * 24 * 60 * 60 - (time.weekday() * 24 * 60 * 60 + time.hour * 60 * 60 + time.minute * 60 + time.second)


def periodic_tasks():
    unauthenticated_user_delete()
    group_code_change()
    # 알림 지우기
    # 포인트 지우기
    Timer(7 * 24 * 60 * 60, periodic_tasks).start()


def unauthenticated_user_delete():
    for user in User.objects.all():
        if not user.is_active:
            user.delete()


def group_code_change():
    for group in Group.objects.all():
        group.code = get_invite_code()
        group.save()
