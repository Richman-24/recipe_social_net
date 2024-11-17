from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from api.recipes.serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from api.users.permissions import IsAdminAuthorOrReadOnly
from api.recipes.filters import IngredientFilter
from recipes.models import Favorite, Ingredient, Recipe, RecipeIngredient, ShoppingList, Tag
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.users.pagination import CustorPageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

class RecipeViewSet(viewsets.ModelViewSet):
    ...



class IngredientsViewSet(viewsets.ReadOnlyModelViewSet): #OK
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ('^name',)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  # Убедитесь, что возвращаете массив

class TagsViewSet(viewsets.ReadOnlyModelViewSet): #OK
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminAuthorOrReadOnly,)
