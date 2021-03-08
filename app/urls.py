from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Pengaturan untuk dokumentasi API (judul, deskripsi dll)
schema_view = get_schema_view(
    openapi.Info(
        title="News App API",
        default_version='001-rz',
        description="An api for News App",
        terms_of_service="/terms/",
        contact=openapi.Contact(email="boykucayy@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('news.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
]
