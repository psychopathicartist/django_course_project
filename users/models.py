from django.contrib.auth.models import AbstractUser
from django.db import models

from mailing.models import NULLABLE


class User(AbstractUser):
    """
    Модель пользователя, переопределенная от AbstractUser,
    основным полем теперь является email, а не username
    """

    username = None

    email = models.EmailField(verbose_name='почта', unique=True)
    full_name = models.CharField(max_length=200, verbose_name='ФИО', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    status = models.BooleanField(default=True, verbose_name='статус пользователя')
    token = models.CharField(max_length=100, verbose_name='токен', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

        permissions = [
            ('change_users_status', 'Can block user'),
        ]
