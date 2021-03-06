from django.db import models
from user.models import User
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
import os, shutil
from datetime import datetime
import urllib
#######################################
# 파일 저장 경로 지정하기 위한 함수들
# group 대표 이미지


def group_thumbnail_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/group_<group.name>/<filename>
    return 'group/group_{0}/thumbnail/{1}'.format(instance.pk, filename)

# 그룹 게시글 첨부 파일
def group_post_uploads_path(instance, filename):
    date_dir = datetime.today().strftime('/%Y/%m/%d/')
    # file will be uploaded to MEDIA_ROOT/group_<group.name>/post/image/<filename>
    return ('group/group_{0}/post/uploads' + date_dir + '{1}').format(instance.group.pk, filename)


# group 존재 여부 확인


def group_exists(pk):
    return bool(Group.objects.filter(pk=pk))
######################################


# 그룹
class Group(models.Model):
    name = models.CharField(verbose_name='그룹명', max_length=30)
    intro = models.TextField(verbose_name='그룹 소개', blank=True)
    maker = models.ForeignKey(
        User, verbose_name='방장', on_delete=models.CASCADE, null=True, related_name='group_maker')
    code = models.CharField(
        verbose_name='초대 코드', max_length=20, null=True, blank=True)  # 랜덤 코드 길이 설정
    image = models.ImageField(
        upload_to=group_thumbnail_path, null=True, blank=True)
    members = models.ManyToManyField(User, blank=True)  # 그룹에 가입한 멤버
    waits = models.ManyToManyField(
        User, blank=True, related_name='waits')  # 가입 대기 멤버
    # status = models.CharField(default="false", max_length=30)  # 초대수락 여부에 따른 상태
    MODE_CHOICES = (
        ('PUBLIC', '공개'),
        ('PRIVATE', '비공개'),
    )
    mode = models.CharField(verbose_name='공개 여부',
                            choices=MODE_CHOICES, max_length=20, default=0)
    interests = models.ManyToManyField(
        'user.User', blank=True, related_name='interests')

    def __str__(self):
        return self.name

    # 그룹 삭제 시 media파일 동시 삭제 
    def delete(self, *args, **kwargs):
        group_dir = './media/group/group_{0}/'.format(self.pk)
        super(Group, self).delete(*args, **kwargs)
        shutil.rmtree(group_dir)
# 그룹 찜 기능


class GroupStar(models.Model):
    user = models.ForeignKey(User, verbose_name='사용자',
                             on_delete=models.CASCADE, related_name='star_user')
    group = models.ForeignKey(
        Group, verbose_name='그룹', on_delete=models.CASCADE, related_name='star_group')

    def __str__(self):
        return self.user.nickname + self.group.name

# 그룹 게시글


class GroupPost(models.Model, HitCountMixin):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='group_writer_person', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name= 'this_group')

    title = models.CharField(verbose_name='제목', max_length=50)
    content = models.TextField(verbose_name='내용')
    # 코드 캡쳐, 실행창 캡쳐와 같은 이미지 업로드
    image = models.ImageField(
        upload_to=group_post_uploads_path, null=True, blank=True)
    # .ent, .sb3 파일 등 소스코드 파일 업로드
    attached_file = models.FileField(
        verbose_name='첨부파일', upload_to=group_post_uploads_path, null=True, blank=True)

    tags = models.ManyToManyField('GroupTag', blank=True)

    GROUP_POST_CATE_CHOICES = (
        ('S', '자랑'),
        ('Q', '질문'),
        ('ETC', '기타'),
    )

    category = models.CharField(
        verbose_name='기본 카테고리', choices=GROUP_POST_CATE_CHOICES, max_length=20, default='기타')

    attached_link = models.URLField(
        verbose_name='첨부된 링크', null=True, blank=True)

    created_at = models.DateTimeField(verbose_name='게시일자', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정일자', auto_now=True)

    like_user = models.ManyToManyField('user.User', blank=True)

    
    ## 매번 iframe과 썸네일 이미지를 크롤링해오느라 느려지지 않도록 textfield 에 저장
    iframe = models.CharField(max_length=200, null=True, blank=True, default='')
    thumbnail_url = models.CharField(max_length=200, null=True, blank=True, default='')


    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    def __str__(self):
        return self.title

    # html 표시용 filename
    def get_filename(self):
        return os.path.basename(self.attached_file.name)

    # 파일 다운로드 용 filname
    def get_filename_download (self):
        file_name = urllib.parse.quote(self.attached_file.name.split('/')[-1].encode('utf-8'))
        return file_name
    
    def delete(self, *args, **kwargs):
        self.attached_file.delete()
        self.image.delete()
        super(GroupPost, self).delete(*args, **kwargs)



# 편의상 댓글, 답변 모두 answer
class GroupAnswer(models.Model):
    
    ### 작성자 필드
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='group_answer_person', null=True, blank=True)

    content = models.TextField(verbose_name='내용')

    created_at = models.DateTimeField(verbose_name='게시일자', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정일자', auto_now=True)

    answer_order = models.IntegerField(verbose_name='답변순서')
    answer_depth = models.IntegerField(verbose_name='답변깊이', default=0)

    post_id = models.ForeignKey(GroupPost, on_delete=models.CASCADE,)

    parent_answer = models.ForeignKey(
        'self', on_delete=models.CASCADE,  null=True, blank=True)
    like_user = models.ManyToManyField('user.User', blank=True)

    is_deleted = models.BooleanField(verbose_name='삭제여부', default=False)

class GroupTag(models.Model):

    tag_name = models.CharField(verbose_name='태그', max_length=20)

    def __str__(self):
        return self.tag_name
