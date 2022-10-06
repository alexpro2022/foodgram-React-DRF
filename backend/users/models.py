from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username

PASSWORD_MAX_LENGTH = 150


class User(AbstractUser):
    email = models.EmailField(
        'Адрес электронной почты', max_length=254, unique=True)
    username = models.CharField(
        'Уникальный юзернейм', max_length=150, unique=True,
        validators=[validate_username])
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    password = models.CharField('Пароль', max_length=PASSWORD_MAX_LENGTH)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    subscribed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Подписанный пользователь')
    author_subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name='Автор подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(  # DONE by get_or_create
                fields=['subscribed_user', 'author_subscription'],
                name='unique_follow'),
            models.CheckConstraint(  # DONE by request.user != author
                check=~models.Q(
                    subscribed_user=models.F('author_subscription')),
                name='no_self_follow'),
        ]
