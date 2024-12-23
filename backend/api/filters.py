from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.NumberFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        user = (
            self.request.user
            if self.request.user.is_authenticated
            else None
        )
        if value and user:
            return queryset.filter(favorites__user_id=user.id)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = (
            self.request.user
            if self.request.user.is_authenticated
            else None
        )
        if value and user:
            return queryset.filter(shopping_lists__user_id=user.id)
        return queryset
