from cmath import pi
from django.db import models
# from django.contrib.auth.models import User
from group.models import *
# from qna.models import *
from django.contrib.auth.models import AbstractUser

#######################################
# 파일 저장 경로 지정하기 위한 함수들
# user 대표 이미지
def user_thumbnail_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<email>/<filename>
    return 'user_{0}/thumbnail/{1}'.format(instance.email, filename)
######################################

class User(AbstractUser):
    email = models.EmailField(verbose_name='email')
    password = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    birth = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to=user_thumbnail_path, null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    total_like = models.IntegerField(null=True, blank=True)
    JOB_CHOICE = (('elementary_school', '초등학생'), ('middle_school', '중학생'), ('high_school', '고등학생'), ('university', '대학생'), ('programmer', '개발자'), ('parents', '학부모'), ('etc', '기타'))
    job = models.CharField(max_length=50, choices=JOB_CHOICE, default='etc')

    def __str__(self):
        return self.nickname

class Reward(models.Model):
    name = models.CharField(max_length=20)
    info = models.TextField()
    img = models.ImageField(upload_to="image/reward_thumbnail", null=True, blank=True)

    def __str__(self):
        return self.name

class GetReward(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reward_id =  models.ForeignKey(Reward, on_delete=models.CASCADE)
    get_date = models.DateTimeField()

class Alert(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    alert_type = models.IntegerField()
    time = models.DateTimeField()