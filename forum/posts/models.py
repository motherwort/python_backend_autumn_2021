from django.db import models
from threads.models import Thread
from users.models import User
from django.utils import timezone


class Post(models.Model):
    created = models.DateTimeField(default=timezone.now, verbose_name='Post creation time')
    is_edited = models.BooleanField(default=False, verbose_name='Is edited')
    is_deleted = models.BooleanField(default=False, verbose_name='Is deleted')
    content = models.TextField(verbose_name='Post content')
    # unedited_content = models.TextField(verbose_name='Unedited content')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # upvotes = ...

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        # not implemented
        return 'localhost:8000/'

    class Meta:
        ordering = ('created',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
