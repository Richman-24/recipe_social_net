from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.static import serve

from api.recipes.views import short_url

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('s/<int:pk>/', short_url, name='short_url')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    urlpatterns += [
        path("redoc/", TemplateView.as_view(template_name="redoc.html"), name="redoc"),
        path(
            "redoc/openapi-schema.yml",
            serve,
            {
                "path": "openapi-schema.yml",
                "document_root": settings.BASE_DIR.parent / "docs",
            },
        ),
    ]

#api/users/
#api/users/<pk: id>/
#api/users/<pk: id>/supscribe/
#api/users/subscription/
#api/users/me/
#api/users/me/avatar/
#api/users/set-password/
#api/users/token/login
#api/users/token/logout
#
#api/recipes/  # выводит список рецептов на главную (нужно добавить фильтры)
#api/recipes/<pk:id>/  # выводит конкретный рецепт
#api/recipes/<pk:id>/get-link/ # делает короткую ссылку для конкретного рецепта
#api/recipes/<pk:id>/shopping-cart/  # добавляет выбранный рецепт в список покупок
#api/recipes/<pk:id>/favorite/  # Добавляет выбранный рецепт в избранное
#api/recipes/download-shoping-cart/  # Функция скачивания корзины.
#
#api/tags/  # Показывает список тэгов GET
#api/tags/<id: pk>/  # показывает конкретный тэг GET
#
#api/ingredients/  # Показывает список ингридиентов GET
#api/ingredients/<pk: id>/  # показывает конкретный ингридиент GET
#
