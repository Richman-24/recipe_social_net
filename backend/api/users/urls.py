from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.users import views

user_router = DefaultRouter()
user_router.register('', views.CustomUserViewSet, basename='users')


users_urls = [
    path('users/', include(user_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]