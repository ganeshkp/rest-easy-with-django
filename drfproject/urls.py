"""
URL configuration for drfproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="DRF Book APIs",
      default_version='v1',
      description="DRF Book APIs Documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    #drf-spectacular URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    #drf-yasg URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('api/chapter6_serializers_views/', include('chapter6_serializers_views.api.urls')),
    path('api/chapter7_viewsets_routers/', include('chapter7_viewsets_routers.api.urls')),
    path('api/chapter8_validators/', include('chapter8_validators.api.urls')),
    path('api/chapter9_authentication/', include('chapter9_authentication.api.urls')),
    path('api/user/', include('user_app.api.urls')),
    path('api/chapter10_permissions/', include('chapter10_permissions.api.urls')),
    path('api/chapter11_caching/', include('chapter11_caching.api.urls')),
    path('api/chapter12_throttling/', include('chapter12_throttling.api.urls')),
    path('api/chapter13_filtering_searching_ordering/', include('chapter13_filtering_searching_ordering.api.urls')),
    path('api/chapter14_pagination/', include('chapter14_pagination.api.urls')),
    path('api/chapter15_versioning/', include('chapter15_versioning.api.urls')),
    path('api/v1/chapter15_versioning/', include(('chapter15_versioning.api.urls', 'chapter15_versioning'), namespace="v1")),
    path('api/v2/chapter15_versioning/', include(('chapter15_versioning.api.urls', 'chapter15_versioning'), namespace="v2")),
    path('api/chapter16_testing/', include('chapter16_testing.api.urls')),
    path('api/chapter17_documenting/', include('chapter17_documenting.api.urls')),
]
