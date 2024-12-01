from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer as US
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from foodgram.constants import PER_PAGE_LIMIT
from recipes.models import Recipe
from users.models import Follow

User = get_user_model()


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(US):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'avatar'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request is not None
            and request.user.is_authenticated
            and request.user.following.exists()
        )


class UserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("user", "author")

    def to_representation(self, instance):
        author = instance.author
        return SubscriberDetailSerializer(author, context=self.context).data

    def validate_author(self, value):
        if self.context['request'].user.id == value.id:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя')
        return value


class SubscriberDetailSerializer(UserSerializer):
    """Сериализатор карточки автора для подписчика."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='following.count')

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = str(request.GET.get('recipes_limit', PER_PAGE_LIMIT))
        response = obj.recipes.all()

        if limit and limit.isdigit():
            response = response[:int(limit)]

        return ShortRecipeSerializer(
            response,
            many=True,
            read_only=True
        ).data


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(allow_null=True)

    class Meta:
        model = User
        fields = ('avatar',)
