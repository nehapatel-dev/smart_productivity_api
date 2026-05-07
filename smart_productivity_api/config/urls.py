"""Root URL configuration with Swagger + ReDoc docs."""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import home

schema_view = get_schema_view(
    openapi.Info(
        title="Smart Productivity & Task Management API",
        default_version="v1",
        description="Secure, scalable task management API with JWT auth, "
                    "categories, filtering, analytics & Swagger docs.",
        contact=openapi.Contact(email="dev@example.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', home, name='home'),
    path("admin/", admin.site.urls),

    # API
    path("api/auth/", include("users.urls")),
    path('api/users/', include('users.urls')),
    path("api/categories/", include("categories.urls")),
    path("api/tasks/", include("tasks.urls")),

    # Docs
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]
