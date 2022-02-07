# Generated by Django 4.0.2 on 2022-02-07 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='게시일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
                ('answer_order', models.IntegerField(verbose_name='답변순서')),
                ('answer_depth', models.IntegerField(default=0, verbose_name='답변깊이')),
            ],
        ),
        migrations.CreateModel(
            name='QnaTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=20, verbose_name='태그')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('image', models.ImageField(blank=True, null=True, upload_to='qna/image')),
                ('attached_file', models.FileField(blank=True, null=True, upload_to='qna/code', verbose_name='첨부파일')),
                ('hit', models.IntegerField(default=0, verbose_name='조회수')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='게시일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
                ('s_or_e_tag', models.CharField(choices=[('S', '스크래치'), ('E', '엔트리'), ('ETC', '기타')], max_length=20, verbose_name='기본 카테고리')),
            ],
        ),
    ]
