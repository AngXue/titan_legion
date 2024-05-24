from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('sso/', include('esi.urls', namespace='esi')),
    path('', include('titan_main.urls', namespace='titan_main')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
