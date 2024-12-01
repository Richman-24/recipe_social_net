from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


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
