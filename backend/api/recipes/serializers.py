from rest_framework import serializers

from api.users.serializers import UserSerializer
from api.serializers import Base64ImageField
from users.models import Follow
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTags,
    ShoppingList,
    Tag
)
from foodgram.constants import PER_PAGE_LIMIT


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода GET list и retrieve тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода GET list и retrieve ингредиентов"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиентов в рецептах list, retrive"""

    id = serializers.IntegerField(source='ingredient_id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов. Поддерживает вывод GET list и retrieve."""

    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = RecipeIngredientSerializer(
        source='ingredients_in_recipe', many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def check_user_status(self, obj, model_class):
        user = self.context.get('request')
        return bool(
            user
            and user.user.is_authenticated
            and model_class.objects.filter(recipe=obj,
                                           user=user.user).exists()
        )

    def get_is_favorited(self, obj):
        return self.check_user_status(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.check_user_status(obj, ShoppingList)


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        label='Tags',
    )
    ingredients = RecipeIngredientWriteSerializer(
        many=True,
        label='Ingredients',
    )
    image = Base64ImageField(
        allow_null=True,
        label='images'
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                'Добавьте категорию')

        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                'Такая категория уже зарегистрированна'
            )

        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                'Добавьте ингридиент'
            )
        ingredient_ids = [ingredient['id'] for ingredient in value]
        existing_ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
        if len(existing_ingredients) != len(ingredient_ids):
            missing_ids = set(ingredient_ids) - set(
                existing_ingredients.values_list('id', flat=True)
            )
            raise serializers.ValidationError(
                f'Ингридиента с id {missing_ids} не существует'
            )
        return value

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(
            instance, context={'request': self.context.get('request')}
        )
        return serializer.data

    def create_tags(self, tags, recipe):
        recipe.tags.set(tags)

    def create_ingredients(self, ingredients, recipe):
        for ingredient_data in ingredients:
            ingredient_id = ingredient_data['id']
            ingredient = Ingredient.objects.get(pk=ingredient_id)
            amount = ingredient_data['amount']
            RecipeIngredient.objects.create(
                ingredient=ingredient, recipe=recipe, amount=amount
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        user = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data, author=user)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.get('tags')
        if tags is None:
            raise serializers.ValidationError(
                {'tags': 'Добавьте категорию'}
            )
        ingredients = validated_data.get('ingredients')
        if ingredients is None:
            raise serializers.ValidationError(
                {'ingredients': 'Добавьте ингридиент'}
            )
        RecipeTags.objects.filter(recipe=instance).delete()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.create_tags(validated_data.pop('tags'), instance)
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriberDetailSerializer(serializers.ModelSerializer):
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


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
