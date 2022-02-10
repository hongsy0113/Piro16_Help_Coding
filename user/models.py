from cmath import pi
from django.db import models
# from django.contrib.auth.models import User
from group.models import *
# from qna.models import *
from django.contrib.auth.models import AbstractUser
from .constants import *

# user 대표 이미지
def user_thumbnail_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<email>/<filename>
    return 'user_{0}/thumbnail/{1}'.format(instance.email, filename)

# reward 대표 이미지
def reward_thumbnail_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<email>/<filename>
    return 'reward_{0}/thumbnail/{1}'.format(instance.name, filename)

class User(AbstractUser):
    email = models.EmailField(verbose_name='email')
    password = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    birth = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to=user_thumbnail_path, null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    total_question_like = models.IntegerField(null=True, blank=True)
    total_comment_like = models.IntegerField(null=True, blank=True)
    total_question = models.IntegerField(null=True, blank=True)
    total_answer = models.IntegerField(null=True, blank=True)
    total_answer_reply = models.IntegerField(null=True, blank=True)
    level = models.CharField(max_length=50, choices=LEVEL, default='level_1')
    job = models.CharField(max_length=50, choices=JOB_CHOICE, default='etc')
    
    def __str__(self):
        return self.nickname

    def points(self):
        for category in JOB_CATEGORY:
            if self.job in JOB_CATEGORY[category]:
                return (self.total_question_like * POINT[category]['question_like']
                + self.total_comment_like * POINT[category]['comment_like']
                + self.total_question * POINT[category]['question']
                + self.total_answer * POINT[category]['answer']
                + self.total_answer_reply * POINT[category]['answer_reply'])
        return 0
    
    def total_like(self):
        return self.total_question_like + self.total_comment_like

    def total_comment(self):
        return self.total_answer + self.total_answer_reply

    def get_level(self):
        for category in JOB_CATEGORY:
            if self.job in JOB_CATEGORY[category]:
                for index in range(len(LEVEL_UP_BOUNDARY[category])):
                    if self.points() >= LEVEL_UP_BOUNDARY[category][index]:
                        level = LEVEL[index]
        self.level = level[0]
        self.save()
        return level[1]
        

class Reward(models.Model):
    name = models.CharField(max_length=20)
    info = models.TextField()
    type = models.CharField(max_length=50, choices=REWARD_TYPE, default='total_like')
    criteria = models.IntegerField(null=True, blank=True)
    img = models.ImageField(upload_to=reward_thumbnail_path, null=True, blank=True)

    def __str__(self):
        return self.name

# 업적 만들기 (현재는 예시임 테스트용)
def initializeReward():
        Reward.objects.create(name = '총 좋아요 수 2개 달성',
                info = '총 좋아요 수 2개 달성',
                type = 'total_like', criteria = 2)
        Reward.objects.create(name = '게시글 좋아요 수 2개 달성',
                info = '게시글 좋아요 수 2개 달성',
                type = 'question_like', criteria = 2)
        Reward.objects.create(name = '댓글 좋아요 수 2개 달성',
                info = '댓글 좋아요 수 2개 달성',
                type = 'comment_like', criteria = 2)
        Reward.objects.create(name = '총 질문 수 2개 달성',
                info = '총 질문 수 2개 달성',
                type = 'total_question', criteria = 2)
        Reward.objects.create(name = '총 답변 수 2개 달성',
                info = '총 답변 수 2개 달성',
                type = 'total_answer', criteria = 2)
        Reward.objects.create(name = '총 댓글 수 2개 달성',
                info = '총 댓글 수 2개 달성',
                type = 'total_comment', criteria = 2)
                
class GetReward(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reward_id =  models.ForeignKey(Reward, on_delete=models.CASCADE)
    get_date = models.DateTimeField()

class Alert(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    alert_type = models.IntegerField()
    time = models.DateTimeField()