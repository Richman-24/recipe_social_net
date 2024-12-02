from django.conf import settings
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.static import serve 

from api.recipes.urls import recipe_urls
from api.users.urls import users_urls

app_name = 'api'


urlpatterns = [
    path('', include(users_urls)),
    path('', include(recipe_urls)),
    path('docs/',
         TemplateView.as_view(template_name='redoc.html'),
         name='redoc'
         ),
    # path(
    #     "docs/openapi-schema.yml",
    #     serve,
    #     {
    #         "path": "openapi-schema.yml",
    #         "document_root": settings.BASE_DIR / "api/docs",
    #     },
    # ),
]
