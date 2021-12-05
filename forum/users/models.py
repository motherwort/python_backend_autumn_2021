from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUnicodeUsernameValidator(UnicodeUsernameValidator):
    regex = r'^[\w.]+\Z'


# TODO remove name
class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits, dots and underlines only.'),
        validators=[CustomUnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(max_length=100, null=True, verbose_name='Name')
    user_info = models.TextField(null=True, verbose_name='User info')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        raise NotImplementedError

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
