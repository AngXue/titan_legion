import logging

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from esi.decorators import token_required
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .esi import get_eve_skill, get_eve_isk
from .models import Profile, Item, Order, Apply
from .scopes import SCOPES_LIST
from .serializers import ProfileSerializer, ItemSerializer, OrderSerializer, ApplySerializer

logging = logging.getLogger(__name__)


def is_authenticated_view(request):
    return JsonResponse({'is_authenticated': request.user.is_authenticated})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('titan_main:home')
    return render(request, 'titan_main/html/login.html')


@login_required
@token_required(scopes=SCOPES_LIST)
def home_view(request, token):
    character_id = token.character_id
    isk = float(get_eve_isk(character_id))
    skill = float(get_eve_skill(character_id)['total_sp'])

    profile = Profile.objects.get(user=request.user)
    profile.isk = isk
    profile.skill = skill
    profile.character_id = character_id
    profile.save()

    return render(request, 'titan_main/html/index.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('titan_main:home')


@login_required
def get_current_user(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile)
    return JsonResponse(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['post'])
    def update_isk_and_skill(self, request, pk=None):
        logging.debug(
            "Update isk and skill request from %s, pk=%s",
            request.user,
            pk
        )
        profile = self.get_object()

        try:
            # 使用装饰器来获取并更新数据
            def update():
                character_id = profile.character_id
                notifications = get_eve_skill(character_id)
                profile.skill = float(notifications['total_sp'])
                isk = get_eve_isk(character_id)
                profile.isk = float(isk)
                profile.save()
                return Response({'status': 'isk and skill updated'})

            # 调用内部函数以更新数据
            return update()

        except Exception as e:
            return Response({'status': 'failed', 'reason': str(e)})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.update_isk_and_skill(request, pk=instance.pk)
        instance.refresh_from_db()  # 刷新对象以获取最新的数据库状态
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        for profile in queryset:
            self.update_isk_and_skill(request, pk=profile.pk)
        queryset = self.get_queryset()  # 重新获取更新后的数据
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ApplyViewSet(viewsets.ModelViewSet):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer
