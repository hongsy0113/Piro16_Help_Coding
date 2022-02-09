# Generated by Django 4.0.2 on 2022-02-08 01:47

from django.db import migrations, models
import django.db.models.deletion
import group.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='그룹명')),
                ('intro', models.TextField(max_length=250, verbose_name='그룹 소개')),
                ('code', models.CharField(blank=True, max_length=20, null=True, verbose_name='초대 코드')),
                ('image', models.ImageField(blank=True, null=True, upload_to=group.models.group_thumbnail_path)),
                ('mode', models.CharField(choices=[('PUBLIC', '공개'), ('PRIVATE', '비공개')], max_length=20, verbose_name='공개 여부')),
                ('star', models.IntegerField(default=0, verbose_name='찜하기 개수')),
                ('is_star', models.BooleanField(default=False, verbose_name='찜하기')),
            ],
        ),
        migrations.CreateModel(
            name='GroupAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='게시일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
                ('answer_order', models.IntegerField(verbose_name='답변순서')),
                ('answer_depth', models.IntegerField(verbose_name='답변깊이')),
            ],
        ),
        migrations.CreateModel(
            name='GroupAnswerReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GroupPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('image', models.ImageField(blank=True, null=True, upload_to=group.models.group_post_img_path)),
                ('attached_file', models.FileField(blank=True, null=True, upload_to=group.models.group_post_code_path, verbose_name='첨부파일')),
                ('hit', models.IntegerField(default=0, verbose_name='조회수')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='게시일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
            ],
        ),
        migrations.CreateModel(
            name='GroupTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=20, verbose_name='태그')),
            ],
        ),
        migrations.CreateModel(
            name='GroupTagging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_post', to='group.grouppost')),
                ('tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='this_group_tag', to='group.grouptag')),
            ],
        ),
        migrations.CreateModel(
            name='GroupPostReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reacted_post', to='group.grouppost')),
            ],
        ),
    ]
