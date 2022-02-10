from django.db import models
from user.models import User
#from qna.models import *

#######################################
# 파일 저장 경로 지정하기 위한 함수들
# group 대표 이미지
def group_thumbnail_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/group_<group.id>/<filename>
    return 'group_{0}/thumbnail/{1}'.format(instance.name, filename)

# group 게시판 이미지
def group_post_img_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/group_<group.id>/<filename>
    return 'group_{0}/image/{1}'.format(instance.id, filename)

# group 게시판 첨부코드
def group_post_code_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/group_<group.id>/<filename>
    return 'group_{0}/code/{1}'.format(instance.id, filename)
######################################

# 그룹
class Group(models.Model):
    name = models.CharField(verbose_name='그룹명', max_length=30)
    intro = models.TextField(verbose_name='그룹 소개', max_length=250, blank=True)
    maker = models.ForeignKey(User, verbose_name='방장', on_delete=models.CASCADE, null=True, related_name='group_maker')
    code = models.CharField(verbose_name='초대 코드', max_length=20, null=True, blank=True)  #랜덤 코드 길이 설정
    image = models.ImageField(upload_to=group_thumbnail_path, null=True, blank=True)
    members = models.ManyToManyField(User, blank=True)  # 그룹에 가입한 멤버
    waits = models.ManyToManyField(User, blank=True, related_name='waits')  # 가입 대기 멤버
    # status = models.CharField(default="false", max_length=30)  # 초대수락 여부에 따른 상태
    MODE_CHOICES = (
        ('PUBLIC', '공개'),
        ('PRIVATE', '비공개'),
    )
    mode = models.CharField(verbose_name='공개 여부', choices=MODE_CHOICES, max_length=20, default=0)
    interests = models.ManyToManyField('user.User', blank=True, related_name='interests')
    is_star = models.BooleanField(verbose_name="찜하기", default=False)
    
    def __str__(self):
        return self.name

# 그룹 게시글
class GroupPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='group_writer_person')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name= 'this_group')

    title = models.CharField(verbose_name='제목', max_length=30)
    content = models.TextField(verbose_name='내용')
    # 코드 캡쳐, 실행창 캡쳐와 같은 이미지 업로드
    image = models.ImageField(upload_to=group_post_img_path, null=True, blank=True)
    # .ent, .sb3 파일 등 소스코드 파일 업로드
    attached_file = models.FileField(verbose_name='첨부파일', upload_to=group_post_code_path, null=True, blank=True)

    tags = models.ManyToManyField('GroupTag', blank=True)

    hit = models.IntegerField(verbose_name='조회수', default=0)

    created_at = models.DateTimeField(verbose_name='게시일자', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정일자', auto_now=True)

    def __str__(self):
        return self.title
    


# 편의상 댓글, 답변 모두 answer
class GroupAnswer(models.Model):
    
    ### 작성자 필드
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='group_answer_person')

    content = models.TextField(verbose_name='내용')

    created_at = models.DateTimeField(verbose_name='게시일자', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정일자', auto_now=True)

    answer_order = models.IntegerField(verbose_name='답변순서')
    answer_depth = models.IntegerField(verbose_name='답변깊이')

    post_id = models.ForeignKey(GroupPost, on_delete=models.CASCADE,)

    parent_answer = models.ForeignKey('self', on_delete=models.CASCADE,)


class GroupPostReaction(models.Model):
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='reacted_post')

    # 리액션한 사람
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_react_person') 


# 답변 리액션
class GroupAnswerReaction(models.Model):
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='reacted_group_answer')

    # 리액션한 사람
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_answer_react_person') 

class GroupTag(models.Model):

    tag_name = models.CharField(verbose_name='태그', max_length=20)

    def __str__(self):
        return self.tag_name
