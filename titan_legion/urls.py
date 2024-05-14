from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from titan_main.views import is_authenticated_view, login_view, home_view, logout_view, eve_auth_view
from titan_main.views import ProfileViewSet, ItemViewSet, OrderViewSet, ApplyViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'items', ItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'applies', ApplyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/profile/', home_view, name='profile'),
    path('accounts/logout/', logout_view, name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('sso/', include('esi.urls', namespace='esi')),
    path('is_authenticated/', is_authenticated_view, name='is_authenticated'),
    path('login/', eve_auth_view, name='login'),
    path('api/', include(router.urls)),
]
