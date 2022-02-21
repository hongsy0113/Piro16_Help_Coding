from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import *
from datetime import datetime
import shutil
# user 대표 이미지


def user_thumbnail_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<email>/<filename>
    return 'user/user_{0}/thumbnail/{1}'.format(instance.email, filename)

# reward 대표 이미지


# def reward_thumbnail_path(instance, filename):
#    # file will be uploaded to MEDIA_ROOT/user_<email>/<filename>
#    return 'reward_{0}/thumbnail/{1}'.format(instance.name, filename)


# 시간
def time_convert(datetimefield):
    data = datetime(datetimefield.year, datetimefield.month, datetimefield.day,
                    datetimefield.hour, datetimefield.minute, datetimefield.second)
    second = int((datetime.now() - data).total_seconds())
    if second > 60 * 60 * 24:
        return str(second // (60 * 60 * 24)) + "일 전"
    elif second > 60 * 60:
        return str(second // (60 * 60)) + "시간 전"
    elif second > 60:
        return str(second // 60) + "분 전"
    else:
        return str(second) + "초 전"


class Reward(models.Model):
    name = models.CharField(max_length=20)
    info = models.TextField()
    type = models.CharField(
        max_length=50, choices=REWARD_TYPE, default='total_like')
    criteria = models.IntegerField(null=True, blank=True)
    img = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def has_reward(self, user):
        if GetReward.objects.get(user=user, reward=self):
            return True
        else:
            return False


class User(AbstractUser):
    email = models.EmailField(verbose_name='email')
    password = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    birth = models.DateField(null=True, blank=True)
    img = models.ImageField(
        upload_to=user_thumbnail_path, null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    total_question_like = models.IntegerField(null=True, blank=True, default=0)
    total_comment_like = models.IntegerField(null=True, blank=True, default=0)
    total_question = models.IntegerField(null=True, blank=True, default=0)
    total_answer = models.IntegerField(null=True, blank=True, default=0)
    total_answer_reply = models.IntegerField(null=True, blank=True, default=0)
    level = models.CharField(max_length=50, choices=LEVEL, default='level_1')
    job = models.CharField(max_length=50, choices=JOB_CHOICE, default='etc')
    representative_reward = models.ForeignKey(
        Reward, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nickname

    def points(self):
        for category in JOB_CATEGORY:
            if self.job in JOB_CATEGORY[category]:
                return (self.total_question_like * POINT[category]['question_like']
                        + self.total_comment_like *
                        POINT[category]['comment_like']
                        + self.total_question * POINT[category]['question']
                        + self.total_answer * POINT[category]['answer']
                        + self.total_answer_reply * POINT[category]['answer_reply'])
        return 0

    def total_like(self):
        return self.total_question_like + self.total_comment_like

    def total_comment(self):
        return self.total_answer + self.total_answer_reply

    def get_level(self):
        current_level = self.level

        for category in JOB_CATEGORY:
            if self.job in JOB_CATEGORY[category]:
                for index in range(len(LEVEL_UP_BOUNDARY[category])):
                    if self.points() >= LEVEL_UP_BOUNDARY[category][index]:
                        level = LEVEL[index]

        if level[0] != current_level:
            if LEVEL_STEP.index(current_level) < LEVEL_STEP.index(level[0]):
                Alert.objects.create(user=self, content="짝짝짝! 레벨이 '{}'로 올라갔어요!".format(
                    LEVEL[LEVEL_STEP.index(level[0])][1]), alert_type="level_up", time=datetime.now())
            else:
                Alert.objects.create(user=self, content="레벨이 '{}'로 변경되었어요.".format(
                    LEVEL[LEVEL_STEP.index(level[0])][1]), alert_type="level_change", time=datetime.now())

        self.level = level[0]
        self.save()
        return level[1]

    def has_new_alert(self):
        new_alert_num = 0
        for alert in Alert.objects.filter(user=self):
            if not alert.checked:
                new_alert_num += 1
        return new_alert_num

    def get_new_alert(self):
        return Alert.objects.filter(user=self, checked=False).order_by('-time')[:3]

    def mypage_description(self):
        my_category = ''
        description = ['열심히 활동해서 포인트를 모으면 레벨을 높일 수 있어요!', '~~~', '💛 레벨 체계']
        for category in JOB_CATEGORY:
            if self.job in JOB_CATEGORY[category]:
                my_category = category
        description += level_description(my_category)
        description += ['~~~', '💛 포인트 체계']
        description += point_description(my_category)
        description += ['~~~', '💛 나의 현황', self.nickname +
                        " 님의 현재 레벨은 " + self.get_level() + ", 포인트는 " + str(self.points()) + "점입니다."]
        if LEVEL_STEP.index(self.level) == len(LEVEL) - 1:
            description += ["이미 최고 레벨에 도달했어요!"]
        else:
            description += ["다음 레벨까지 " + str(
                LEVEL_UP_BOUNDARY[my_category][LEVEL_STEP.index(self.level) + 1] - self.points()) + "점이 더 필요해요!"]
        return description

    def delete(self, *args, **kwargs):
        user_dir = './media/user/user_{0}/'.format(self.email)
        super(User, self).delete(*args, **kwargs)
        shutil.rmtree(user_dir)
        


class GetPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=50, choices=POINT_TYPE, default='question_like')
    point = models.IntegerField(null=True, blank=True)
    get_date = models.DateTimeField()

    def time_past(self):
        return time_convert(self.get_date)


# 업적 만들기 (현재는 예시임 테스트용)


def initializeReward():
    for REWARD in REWARD_ALL:
        if not Reward.objects.filter(name=REWARD[0]):
            Reward.objects.create(
                name=REWARD[0], info=REWARD[1], type=REWARD[2], criteria=REWARD[3], img=REWARD[4])


class GetReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    get_date = models.DateTimeField()


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    alert_type = models.CharField(
        max_length=50, choices=ALERT_TYPE, default='etc')
    time = models.DateTimeField()
    related_id = models.CharField(max_length=100, default='')
    checked = models.BooleanField(default=False)

    def related_url(self):
        if self.alert_type in ['new_comment_qna', 'new_reply_qna']:
            # related_id : question id
            return '/qna/{}/'.format(self.related_id)
        elif self.alert_type in ['new_comment_group', 'new_reply_group']:
            # related_id : group id + " " + post id
            return '/group/{}/post_detail/{}'.format(self.related_id.split(" ")[0], self.related_id.split(" ")[1])
        elif self.alert_type in ['level_up', 'level_change']:
            return '/mypage/point/'
        elif self.alert_type in ['get_reward']:
            return '/mypage/reward/'
        elif self.alert_type in ['group_create', 'group_join', 'group_reject', 'group_register', 'group_maker']:
            # if Group.objects.filter(pk=self.related_id):
            return '/group/{}/group_detail/'.format(self.related_id)
            # else:
            #    return '#'
        else:
            return '#'

    def time_past(self):
        return time_convert(self.time)
