from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import Follow

User = get_user_model()


class SubscriptionTabAdmin(admin.TabularInline):
    model = Follow
    list_display = ('id', 'user', 'author')
    fk_name = 'user'
    extra = 0


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'id',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'first_name')
    search_fields = ('username', 'email')
    empty_value_display = '-empty-'

    inlines = (SubscriptionTabAdmin,)