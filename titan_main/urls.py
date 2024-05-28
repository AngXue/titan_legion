from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .esi import eve_auth_view

app_name = 'titan_main'

router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'applies', views.ApplyViewSet)

urlpatterns = [
    path('', views.home_view, name='home'),
    path('lpshop/', views.lpshop_view, name='lpshop'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('is_authenticated/', views.is_authenticated_view, name='is_authenticated'),
    path('get_token_view/', views.get_token_view, name='get_token_view'),
    path('get_current_user/', views.get_current_user, name='get_current_user'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('eve_auth/', eve_auth_view, name='eve_auth'),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
