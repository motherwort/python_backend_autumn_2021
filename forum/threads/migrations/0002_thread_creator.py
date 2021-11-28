# Generated by Django 3.2.9 on 2021-11-27 22:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('threads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='threadstarter', to=settings.AUTH_USER_MODEL),
        ),
    ]