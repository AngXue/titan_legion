import logging

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from esi.decorators import token_required
from rest_framework import viewsets
from rest_framework.response import Response

from .esi import get_eve_skill, get_eve_isk
from .models import Profile, Item, Order, Apply
from .paps import get_legion_pap
from .scopes import SCOPES_LIST
from .serializers import ProfileSerializer, ItemSerializer, OrderSerializer, ApplySerializer

logging = logging.getLogger(__name__)


def update_profile_isk_pap_skill(user, character_id):
    try:
        profile = Profile.objects.get(user=user)

        isk = float(get_eve_isk(character_id))
        pap = float(get_legion_pap(user.username))
        skill = float(get_eve_skill(character_id)['total_sp'])

        profile.isk = isk
        profile.skill = skill
        profile.pap = pap
        profile.character_id = character_id
        profile.save()
    except Exception as e:
        logging.debug(
            "Update user:%s isk, pap, skill error!\n%s",
            user.username, str(e)
        )
        return False
    return True


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
    update_profile_isk_pap_skill(request.user, character_id)
    return render(request, 'titan_main/html/index.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('titan_main:home')


@login_required
def get_current_user(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile)
    profile = serializer.data
    return JsonResponse({'username': request.user.username, 'profile': profile})


@login_required
def upload_item_image(request):
    # TODO: 上传商品图片到媒体目录
    pass


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        update_profile_isk_pap_skill(request.user, instance.character_id)
        instance.refresh_from_db()  # 刷新对象以获取最新的数据库状态
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        for profile in queryset:
            update_profile_isk_pap_skill(request.user, profile.character_id)
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
