from django.db import models
from pools.models import Pool


class Thread(models.Model):
    title = models.CharField(max_length=200, verbose_name='Thread title')
    description = models.TextField(verbose_name='Thread description')
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, verbose_name='Thread pool id')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # not implemented
        return 'localhost:8000/'

    class Meta:
        ordering = ('pool', 'title')
        verbose_name = 'Тред'
        verbose_name_plural = 'Треды'
