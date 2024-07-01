from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('social-auth/', include('social_django.urls', namespace='social')),
                  path('sso/', include('esi.urls', namespace='esi')),
                  path('', include('titan_main.urls', namespace='titan_main')),
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # redoc接口文档
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
