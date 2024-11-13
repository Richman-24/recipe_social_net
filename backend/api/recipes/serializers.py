from rest_framework import serializers

from recipes.models import Recipe, RecipeIngredient, Tag


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient_id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    unit = serializers.ReadOnlyField(source='ingredient.unit')
    
    class Meta:
        fields = ('id', 'name', 'unit', 'amount')
        model = RecipeIngredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient_id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    unit = serializers.ReadOnlyField(source='ingredient.unit')
    
    class Meta:
        fields = ('id', 'name', 'unit', 'amount')
        model = RecipeIngredient


class RecipeSerializer(serializers.ModelSerializer):
    ingredient = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True)

    class Meta:
        fields = (
            'id', 'tag', 'author', 'ingredient',
            'name', 'description', 'cooking_time', 'image'
        )
        read_only_fields = ('author',)
        model = Recipe
