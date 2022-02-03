# Generated by Django 4.0.2 on 2022-02-03 18:58

from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_company', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('info', models.TextField()),
                ('img', models.ImageField(blank=True, null=True, upload_to='image/reward_thumbnail')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('birth', models.DateField(blank=True, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to=user.models.user_thumbnail_path)),
                ('introduction', models.TextField(blank=True, null=True)),
                ('total_like', models.IntegerField(blank=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.job')),
            ],
        ),
        migrations.CreateModel(
            name='GetReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('get_date', models.DateTimeField()),
                ('reward_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.reward')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('alert_type', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
