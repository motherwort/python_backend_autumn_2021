# Generated by Django 3.2.9 on 2021-11-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Is deleted'),
        ),
        migrations.AddField(
            model_name='post',
            name='is_edited',
            field=models.BooleanField(default=False, verbose_name='Is edited'),
        ),
    ]
