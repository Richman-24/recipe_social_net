from django.core.exceptions import ValidationError
from django.conf import settings

from foodgram.constants import ERROR_MESSAGE


def reserved_names_validator(value):
    """Валидация имени пользователя."""

    if value.lower() in settings.RESERVED_USERNAMES:
        raise ValidationError(
            ERROR_MESSAGE['reserved_name_error']
        )