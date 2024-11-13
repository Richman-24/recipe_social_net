from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.users import views

router = DefaultRouter()
router.register('', views.CustomUserViewSet, basename='users')


users_urls = [
    path('users/', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]