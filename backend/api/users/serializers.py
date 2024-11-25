from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.serializers import Base64ImageField
from recipes.models import Recipe
from users.models import Follow
from foodgram.constants import PER_PAGE_LIMIT

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(allow_null=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'password',
            'first_name', 'last_name',
            'is_subscribed', 'avatar'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return request.user.follower.filter(author=obj).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
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


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriberDetailSerializer(serializers.ModelSerializer):
    """Сериализатор карточки автора для подписчика"""

    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    avatar = Base64ImageField(source='author.avatar')

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return Follow.objects.filter(author=obj.author, user=user).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit', PER_PAGE_LIMIT)
        try:
            limit = int(limit)
        except ValueError:
            pass
        return ShortRecipeSerializer(
            Recipe.objects.filter(author=obj.author)[:limit],
            many=True,
            context={'request': request},
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(allow_null=True)

    class Meta:
        model = User
        fields = ('avatar',)


class SubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'

    def to_representation(self, instance):
        return SubscriberDetailSerializer(instance, context=self.context).data

    def validate_author(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя')
        return value
