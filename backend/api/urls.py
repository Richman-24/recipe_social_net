from django.urls import include, path

from api.recipes.urls import recipe_urls
from api.users.urls import users_urls

app_name = 'api'


urlpatterns = [
    path('', include(users_urls)),
    path('', include(recipe_urls)),
]
