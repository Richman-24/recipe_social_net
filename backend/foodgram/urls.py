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
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

    urlpatterns += [
        path(
            "redoc/",
            TemplateView.as_view(template_name="redoc.html"),
            name="redoc"
        ),
        path(
            "redoc/openapi-schema.yml",
            serve,
            {
                "path": "openapi-schema.yml",
                "document_root": settings.BASE_DIR.parent / "docs",
            },
        ),
    ]
