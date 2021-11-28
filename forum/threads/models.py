from django.db import models
from pools.models import Pool
from users.models import User


class Thread(models.Model):
    title = models.CharField(max_length=200, verbose_name='Thread title')
    description = models.TextField(verbose_name='Thread description')
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='threadstarter')
    # latest_activity = ...
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, verbose_name='Thread pool id')

    # МБ стоит создать одно поле с json, содерж данные до изменений?
    # unedited_title = models.CharField(max_length=100, verbose_name='Unedited title')
    # unedited_description = models.TextField(null=True, verbose_name='Unedited description')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # not implemented
        return 'localhost:8000/'

    class Meta:
        ordering = ('pool', 'title') # ('latest_activity', 'pool', 'title') 
        verbose_name = 'Тред'
        verbose_name_plural = 'Треды'
