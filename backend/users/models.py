from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from foodgram.constants import (
    USER_LENGTH_LIMIT,
    EMAIL_LENGTH_LIMIT
)

username_validator = UnicodeUsernameValidator()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя с email вместо username."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        max_length=USER_LENGTH_LIMIT,
        unique=True,
        validators=(username_validator,)
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

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

    def __str__(self):
        return f'Подписчик {self.user}'
