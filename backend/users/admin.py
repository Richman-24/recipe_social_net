from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import Follow

User = get_user_model()


class SubscriptionTabAdmin(admin.TabularInline):
    model = Follow
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    fk_name = 'user'
    verbose_name = 'Подписка'
    verbose_name_plural = 'Подписки'
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'author')


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
    empty_value_display = '-empty-'

    inlines = (SubscriptionTabAdmin,)

    def get_inline_instances(self, request, obj=None, **kwargs):
        self.parent_object = obj
        return super().get_inline_instances(request, obj, **kwargs)
