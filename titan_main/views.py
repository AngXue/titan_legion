from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import viewsets
from .scopes import SCOPES_LIST
from .models import Profile, Item, Order, Apply
from .serializers import ProfileSerializer, ItemSerializer, OrderSerializer, ApplySerializer


def is_authenticated_view(request):
    return JsonResponse({'is_authenticated': request.user.is_authenticated})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('titan_main:home')
    return render(request, 'titan_main/html/login.html')


@login_required
def home_view(request):
    return render(request, 'titan_main/html/index.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('titan_main:home')


@login_required
def get_current_user(request):
    return JsonResponse({'user': request.user})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # TOTO: 添加对isk、skill属性查询前自动调用esi接口刷新数据


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ApplyViewSet(viewsets.ModelViewSet):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer
