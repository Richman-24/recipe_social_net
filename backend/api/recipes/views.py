from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from api.recipes.serializers import (
    FavoriteRecipeSerializer,
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer
)
from api.permissions import IsAdminAuthorOrReadOnly
from api.filters import IngredientFilter, RecipeFilter
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingList,
    Tag
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.pagination import CustorPageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsAdminAuthorOrReadOnly
from django.views.decorators.http import require_GET
from django.db.models import Sum


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustorPageNumberPagination
    permission_classes = (IsAdminAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @staticmethod
    def shopping_list_to_txt(ingredients):
        return '\n'.join(
            f'{ingredient["ingredient__name"]} - {ingredient["sum"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            for ingredient in ingredients
        )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'get-link'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

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
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if ShoppingList.objects.filter(recipe=recipe, user=user).exists():
            return Response(
                {
                    'detail': f'Рецепт "{recipe.name}" уже добавлен в корзину'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        ShoppingList.objects.create(recipe=recipe, user=user)
        serializer = FavoriteRecipeSerializer(
            recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        cart_item = ShoppingList.objects.filter(recipe__id=pk, user=user)
        if cart_item.exists():
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                'detail': f'Рецепт "{recipe.name}" не найден'
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

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
                recipe__shopping_list__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(sum=Sum('amount'))
        )
        shopping_list = self.shopping_list_to_txt(ingredients)
        return HttpResponse(shopping_list, content_type='text/plain')

    @action(
        detail=True,
        methods=('POST',),
        permission_classes=[IsAuthenticated],
        url_path='favorite',
        url_name='favorite',
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if Favorite.objects.filter(recipe=recipe,
                                   user=user).exists():
            return Response(
                {'detail': f'Рецепт "{recipe.name}" уже добавлен в избранное'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Favorite.objects.create(recipe=recipe, user=user)
        serializer = FavoriteRecipeSerializer(
            recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        favorite_entry = Favorite.objects.filter(
            recipe=recipe, user=user)
        if favorite_entry.exists():
            favorite_entry.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'detail': f'Рецепта "{recipe.name}" нет в избранном.'},
            status=status.HTTP_400_BAD_REQUEST,
        )


@require_GET
def short_url(request, pk):
    try:
        Recipe.objects.filter(pk=pk).exists()
        return redirect(f'/recipes/{pk}/')
    except Exception:
        raise ValidationError(f'Рецепт "{pk}" не существует.')


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ('^name',)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminAuthorOrReadOnly,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
