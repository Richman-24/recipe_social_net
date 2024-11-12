from django.shortcuts import render


from api.serializers import RecipeSerializer
from recipe.models import Recipe
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
class CreateListRetrievePatchViewSet(mixins.CreateModelMixin,
                                     mixins.DestroyModelMixin,
                                     mixins.ListModelMixin,
                                     mixins.RetrieveModelMixin,
                                     GenericViewSet):
    ...


class RecipeViewSet(CreateListRetrievePatchViewSet):
    """
    Главная страница - выводит список рецептов
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]