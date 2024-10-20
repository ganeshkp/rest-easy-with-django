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

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/watch/', include('watchlist_app.api.urls')),
    # path('api/chapter3_project_setup/', include('chapter3_project_setup.api.urls')),
    path('api/chapter6_serializers_views/', include('chapter6_serializers_views.api.urls')),
    path('api/chapter7_viewsets_routers/', include('chapter7_viewsets_routers.api.urls')),
    path('api/chapter8_validators/', include('chapter8_validators.api.urls')),
    path('api/chapter9_authentication/', include('chapter9_authentication.api.urls')),
    path('api/user/', include('user_app.api.urls')),
    path('api/chapter10_permissions/', include('chapter10_permissions.api.urls')),
]
