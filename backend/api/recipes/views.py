from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from api.recipes.serializers import RecipeSerializer
from recipes.models import Recipe


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


class RecipeViewSet(GenericViewSet):
    ...


class IngredientsViewSet(GenericViewSet):
    ...


class TagsViewSet(GenericViewSet):
    ...

