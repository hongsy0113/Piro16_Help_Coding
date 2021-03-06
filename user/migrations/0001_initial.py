# Generated by Django 3.2.12 on 2022-02-19 01:26

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('password', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('birth', models.DateField(blank=True, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to=user.models.user_thumbnail_path)),
                ('introduction', models.TextField(blank=True, null=True)),
                ('total_question_like', models.IntegerField(blank=True, default=0, null=True)),
                ('total_comment_like', models.IntegerField(blank=True, default=0, null=True)),
                ('total_question', models.IntegerField(blank=True, default=0, null=True)),
                ('total_answer', models.IntegerField(blank=True, default=0, null=True)),
                ('total_answer_reply', models.IntegerField(blank=True, default=0, null=True)),
                ('level', models.CharField(choices=[('level_1', '1단계'), ('level_2', '2단계'), ('level_3', '3단계'), ('level_4', '4단계'), ('level_5', '5단계')], default='level_1', max_length=50)),
                ('job', models.CharField(choices=[('elementary_school', '초등학생'), ('middle_school', '중학생'), ('high_school', '고등학생'), ('university', '대학생'), ('programmer', '개발자'), ('parents', '학부모'), ('teacher', '교사'), ('etc', '기타')], default='etc', max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('info', models.TextField()),
                ('type', models.CharField(choices=[('total_like', '총 좋아요 수'), ('question_like', '게시글 좋아요 수'), ('comment_like', '댓글 좋아요 수'), ('total_question', '총 질문 수'), ('total_answer', '총 답변 수'), ('total_comment', '총 댓글 수'), ('total_group_joined', '총 가입한 그룹 수'), ('total_group_created', '총 개설한 그룹 수 (위임 포함)'), ('total_group_post', '그룹에서 공유한 글 수')], default='total_like', max_length=50)),
                ('criteria', models.IntegerField(blank=True, null=True)),
                ('img', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GetReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('get_date', models.DateTimeField()),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.reward')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GetPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('question_like', '질문에 대한 좋아요 획득'), ('comment_like', '댓글에 대한 좋아요 획득'), ('question', '질문 작성'), ('answer', '답변 작성'), ('answer_reply', '대댓글 작성'), ('question_like_cancel', '질문에 대한 좋아요 취소'), ('comment_like_cancel', '댓글에 대한 좋아요 취소'), ('question_cancel', '질문 삭제'), ('answer_cancel', '답변 삭제'), ('answer_reply_cancel', '대댓글 삭제')], default='question_like', max_length=50)),
                ('point', models.IntegerField(blank=True, null=True)),
                ('get_date', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('alert_type', models.CharField(choices=[('level_up', '레벨 상승'), ('level_change', '레벨 변경'), ('get_reward', '배지 획득'), ('new_comment_qna', '새 댓글 (묻고 답하기)'), ('new_reply_qna', '새 대댓글 (묻고 답하기)'), ('new_comment_group', '새 댓글 (내 그룹)'), ('new_reply_group', '새 대댓글 (내 그룹)'), ('group_create', '그룹 생성'), ('group_join', '그룹 가입'), ('group_reject', '그룹 거절'), ('group_register', '그룹 가입 신청'), ('group_delete', '그룹 삭제'), ('group_drop', '그룹 탈퇴'), ('group_maker', '그룹 대표 위임'), ('etc', '기타')], default='etc', max_length=50)),
                ('time', models.DateTimeField()),
                ('related_id', models.CharField(default='', max_length=100)),
                ('checked', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='representative_reward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.reward'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
