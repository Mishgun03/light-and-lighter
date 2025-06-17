"""
URL configuration for LightAndLighter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from market.urls import api_patterns, user_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Эндпоинты для аутентификации
    path('auth/', include('users.urls')),
    # Эндпоинты для рыночных данных
    path('api/', include(api_patterns)),
    path('user/', include(user_patterns)),

    # --- ДОКУМЕНТАЦИЯ API ---
    # URL для скачивания файла schema.yml
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI: интерактивная документация
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc: альтернативный вид документации
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
