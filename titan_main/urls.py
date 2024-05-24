from .esi import eve_auth_view
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'titan_main'

router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'applies', views.ApplyViewSet)

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('is_authenticated/', views.is_authenticated_view, name='is_authenticated'),
    path('eve_auth/', eve_auth_view, name='eve_auth'),
    path('api/', include(router.urls)),
]
