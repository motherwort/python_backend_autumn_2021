from django.db import models
from threads.models import Thread
from users.models import User
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    created = models.DateTimeField(default=timezone.now, verbose_name='Post creation time')
    content = models.TextField(verbose_name='Post content')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        # not implemented
        return 'localhost:8000/'

    class Meta:
        ordering = ('created',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
