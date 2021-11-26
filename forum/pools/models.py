from django.db import models
from users.models import User
from django.utils import timezone


class Pool(models.Model):
    name = models.CharField(max_length=100, verbose_name='Pool name')
    description = models.TextField(null=True, verbose_name='Pool description')
    created = models.DateTimeField(default=timezone.now, verbose_name='Pool creation time')
    users = models.ManyToManyField(User, verbose_name='Pool users')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        raise NotImplementedError

    class Meta:
        ordering = ('name', 'created')
        verbose_name = 'Пул'
        verbose_name_plural = 'Пулы'
