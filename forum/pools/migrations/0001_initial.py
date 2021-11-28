# Generated by Django 3.2.9 on 2021-11-26 18:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Pool name')),
                ('description', models.TextField(null=True, verbose_name='Pool description')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Pool creation time')),
            ],
            options={
                'verbose_name': 'Пул',
                'verbose_name_plural': 'Пулы',
                'ordering': ('name', 'created'),
            },
        ),
    ]