from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class TagSerializer(serializers.ModelSerializer): #OK
    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer): #OK

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient_id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    ingredient = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tag', 'author', 'ingredient',
            'name', 'description', 'cooking_time', 'image'
        )
        read_only_fields = ('author',)

