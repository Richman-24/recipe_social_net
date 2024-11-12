from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('recipes', views.RecipeViewSet, basename='recipe')


urlpatterns = [
    path('', include(router_v1.urls))
]
