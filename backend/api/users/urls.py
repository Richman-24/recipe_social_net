from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.users import views

user_urls = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
