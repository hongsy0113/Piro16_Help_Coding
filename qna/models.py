from django.db import models
from user.models  import User
from group.models  import *
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
import os
import urllib

# Create your models here.
class Question(models.Model, HitCountMixin):
    title = models.CharField(verbose_name='제목', max_length=50)
    content = models.TextField(verbose_name='내용')

    # 코드 캡쳐, 실행창 캡쳐와 같은 이미지 업로드
    image = models.ImageField(upload_to='qna/uploads/%Y/%m/%d/', null=True, blank=True)

    # .ent, .sb3 파일 등 소스코드 파일 업로드
    attached_file = models.FileField(verbose_name='첨부파일', upload_to='qna/uploads/%Y/%m/%d/', null=True, blank=True)
    hit = models.IntegerField(verbose_name='조회수', default=0)
    created_at = models.DateTimeField(verbose_name='게시일자', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정일자', auto_now=True)
    SE_TAG_CHOICES = (
        ('S', '스크래치'),
        ('E', '엔트리'),
        ('ETC', '기타'),
    )
    s_or_e_tag = models.CharField(verbose_name='기본 카테고리',choices=SE_TAG_CHOICES, max_length=20)

    #### 직성자필드
    user = models.ForeignKey(User, on_delete=models.SET_NULL ,related_name='question_person', null=True, blank=True)
    like_user = models.ManyToManyField('user.User', blank=True)
    tags = models.ManyToManyField('QnaTag', blank=True)

    def __str__(self):
        return self.title

    # html 표시용 filename
    def get_filename(self):
        return os.path.basename(str(self.attached_file))

    # 파일 다운로드 용 filname
    def get_filename_download (self):
        file_name = urllib.parse.quote(self.attached_file.name.split('/')[-1].encode('utf-8'))
        return file_name

    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    def delete(self, *args, **kwargs):
        self.attached_file.delete()
        self.image.delete()
        super(Question, self).delete(*args, **kwargs)

class Answer(models.Model):
    #####
    ### 작성자 필드
    user = models.ForeignKey(User, on_delete=models.SET_NULL ,related_name='answer_person', null=True, blank=True)
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(verbose_name='게시일자', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정일자', auto_now=True)
    answer_order = models.IntegerField(verbose_name='답변순서')
    answer_depth = models.IntegerField(verbose_name='답변깊이', default=0)

    question_id = models.ForeignKey(Question, on_delete=models.CASCADE,)

    parent_answer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    like_user = models.ManyToManyField('user.User', blank=True)

    is_deleted = models.BooleanField(verbose_name='삭제여부', default=False)

class QnaTag(models.Model):
    # 스크래치 메뉴
    S_TAG_CHOICES = (
        ('MOTION', '동작'),
        ('LOOKS', '형태'),
        ('SOUND', '소리'),
        ('EVENTS', '이벤트'),
        ('CONTROL', '제어'),
        ('SENSING', '감지'),
        ('OPERATORS', '연산'),
        ('VARIABLES', '변수'),
        ('MY', '내 블록'),
        ('ETC', '기타'),
    )

    '''
    # 엔트리 메뉴
    E_TAG_CHOICES = (
        ('START', '시작'),
        ('FLOW', '흐름'),
        ('MOTION', '움직임'),
        ('LOOKS', '생김새'),
        ('BRUSH', '붓'),
        ('SOUND', '소리'),
        ('DECISION', '판단'),
        ('CALCULATE', '계산'),
        ('VARIABLE', '자료'),
        ('FUNCTION', '함수'),
        ('TABLE_AND_AI', '데이터분석 및 인공지능'),
        ('EXTENSION_AND_HARDWARE', '확장 및 하드웨어'),
        ('PYTHON', '엔트리파이썬'),
        ('ETC', '기타'),
    )
    '''
    tag_name = models.CharField(verbose_name='태그',  max_length=20)

    def __str__(self):
        return self.tag_name

