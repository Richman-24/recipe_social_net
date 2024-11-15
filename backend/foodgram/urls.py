from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
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
#api/recipes/
#api/recipes/<pk:id>/
#api/recipes/<pk:id>/get-link/
#api/recipes/<pk:id>/shopping-cart/
#api/recipes/<pk:id>/favorite/
#api/recipes/download-shoping-cart/
#
#api/tags/
#api/tags/<id: pk>/
#
#api/ingredients/
#api/ingredients/<pk: id>/
#
