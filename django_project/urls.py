from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="Chatapp API",
        default_version="v1",
        description="api for real-time chatapp",
        contact=openapi.Contact(email="anuragkt20@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(TokenAuthentication,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chatapp/", include("chatapp.urls")),
    path(
        "chatapp/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
