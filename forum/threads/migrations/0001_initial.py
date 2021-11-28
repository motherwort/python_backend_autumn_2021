# Generated by Django 3.2.9 on 2021-11-26 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Thread title')),
                ('description', models.TextField(verbose_name='Thread description')),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.pool', verbose_name='Thread pool id')),
            ],
            options={
                'verbose_name': 'Тред',
                'verbose_name_plural': 'Треды',
                'ordering': ('pool', 'title'),
            },
        ),
    ]
