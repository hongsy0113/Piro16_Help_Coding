from cmath import pi
from django.db import models
# from django.contrib.auth.models import User
from group.models import *

#from qna.models import *


#######################################
# 파일 저장 경로 지정하기 위한 함수들
# group 대표 이미지
def user_thumbnail_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/group_<group.id>/<filename>
    return 'group_{0}/thumbnail/{1}'.format(instance.id, filename)


######################################


class Job(models.Model):
    school_company = models.CharField(max_length=50)
    def __str__(self):
        return self.school_company
    
class User(models.Model):
    # 장고 모델 상속하는 걸로 해야 함
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    birth = models.DateField(null=True, blank=True)
    # 유저 대표 이미지 
    img = models.ImageField(upload_to=user_thumbnail_path, null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    total_like = models.IntegerField(null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

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