from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET
from django_filters.rest_framework import DjangoFilterBackend
from io import BytesIO
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.recipes import serializers as recipe_serial
from api.users import serializers as user_serial
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingList,
    Tag
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related()
    permission_classes = (IsAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @staticmethod
    def shopping_list_to_txt(ingredients):
        return '\n'.join(
            f'{ingredient["ingredient__name"]} - {ingredient["sum"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            for ingredient in ingredients
        )

    @staticmethod
    def add_to_list(request, pk, model, serializer_class):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        serializer = serializer_class(data={'user': user.id, "recipe": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = user_serial.ShortRecipeSerializer(
            recipe, context={'request': request}
        )
        return Response(response.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_from_list(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if not model.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'errors': f'Рецепт "{recipe.name}" не найден'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item = get_object_or_404(model, user=user, recipe=recipe)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'get-link'):
            return recipe_serial.RecipeReadSerializer
        return recipe_serial.RecipeWriteSerializer

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=[AllowAny],
        url_path='get-link',
        url_name='get-link',
    )
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        rev_link = reverse('short_url', args=[recipe.pk])
        return Response({'short-link': request.build_absolute_uri(rev_link)},
                        status=status.HTTP_200_OK,)

    @action(
        detail=True,
        methods=('POST',),
        permission_classes=[IsAuthenticated],
        url_path='shopping_cart',
        url_name='shopping_cart',
    )
    def shopping_cart(self, request, pk):
        return self.add_to_list(
            request, pk, ShoppingList, recipe_serial.ShoppingListSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_from_list(request, pk, ShoppingList)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_lists__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(sum=Sum('amount'))
        )
        shopping_list_text = self.shopping_list_to_txt(ingredients)

        buffer = BytesIO()
        buffer.write(shopping_list_text.encode('utf-8'))
        buffer.seek(0)

        response = FileResponse(buffer, content_type='text/plain')
        response['Content-Disposition'] = \
            'attachment; filename="shopping_cart.txt"'
        return response

    @action(
        detail=True,
        methods=('POST',),
        permission_classes=[IsAuthenticated],
        url_path='favorite',
        url_name='favorite',
    )
    def favorite(self, request, pk):
        return self.add_to_list(
            request, pk, Favorite, recipe_serial.FavoriteSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_from_list(request, pk, Favorite)


@require_GET
def short_url(request, pk):
    try:
        Recipe.objects.filter(pk=pk).exists()
        return redirect(f'/recipes/{pk}/')
    except Exception:
        raise ValidationError(f'Рецепт "{pk}" не существует.')


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = recipe_serial.IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ('^name',)

    # Я бы рад, босс, но без этого не отображаются тэги, почему-то.
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = recipe_serial.TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
