from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from foodgram.constants import EMAIL_LENGTH_LIMIT, USER_LENGTH_LIMIT
from users.validators import reserved_names_validator

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    username = models.CharField(
        max_length=USER_LENGTH_LIMIT,
        unique=True,
        validators=(username_validator, reserved_names_validator)
    )
    first_name = models.CharField(
        max_length=USER_LENGTH_LIMIT,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=USER_LENGTH_LIMIT,
        verbose_name="Фамилия"
    )

    avatar = models.ImageField(
        upload_to='media/user_images/',
        blank=True, null=True,
        verbose_name="Аватар"
    )
    email = models.EmailField(max_length=EMAIL_LENGTH_LIMIT, unique=True)

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.get_full_name()


class Follow(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_following'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='check_follower_author',
            ),
        ]
        ordering = ('author__username',)

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
