from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.recipes import views

router_v1 = DefaultRouter()
router_v1.register('recipes', views.RecipeViewSet, basename='recipes')


recipe_urls = [
    path('', include(router_v1.urls))
]
