from django.db import models
from user.models import *

class Group(models.Model):
    name = models.CharField(verbose_name="그룹명", max_length=30)
    intro = models.TextField(verbose_name="그룹 소개", max_length=250)
    maker = models.CharField(verbose_name="방장")
    code = models.CharField(verbose_name="초대 코드", max_length=6, null=True)  #랜덤 코드 길이 설정

class Participation(models.Model):
    group = models.ForeignKey(Group, verbose_name="소속 그룹명", blank=True, on_delete=models.CASCADE)
    member = models.ForeignKey(User, verbose_name="그룹멤버")