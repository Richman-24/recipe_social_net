from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.recipes import views

recipe_router = DefaultRouter()
recipe_router.register('recipes', views.RecipeViewSet, basename='recipes')
recipe_router.register(
    'ingredients', views.IngredientsViewSet, basename='ingredients'
)
recipe_router.register('tags', views.TagsViewSet, basename='tags')


recipe_urls = [
    path('', include(recipe_router.urls))
]
