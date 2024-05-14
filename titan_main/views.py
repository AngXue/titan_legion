from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from esi.decorators import token_required
from esi.clients import EsiClientProvider
from esi.models import Token
from .scopes import SCOPES_LIST
from rest_framework import viewsets
from .models import Profile, Item, Order, Apply
from .serializers import ProfileSerializer, ItemSerializer, OrderSerializer, ApplySerializer

esi = EsiClientProvider(app_info_text="titan-legion-management-system v0.0.1")


def is_authenticated_view(request):
    return JsonResponse({'is_authenticated': request.user.is_authenticated})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'titan_main/html/login.html')


@login_required
def home_view(request):
    return render(request, 'titan_main/html/index.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def eve_auth_view(request):
    return redirect('social:begin', 'eveonline')


@token_required(scopes=SCOPES_LIST)
def temp(request, token):
    character_id = token.character_id
    required_scopes = ['esi-skills.read_skillqueue.v1']

    # get a token
    token = Token.get_token(character_id, required_scopes)

    # call the endpoint
    notifications = esi.client.Skills.get_characters_character_id_skillqueue(
        character_id=character_id,
        token=token.valid_access_token()
    ).result()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ApplyViewSet(viewsets.ModelViewSet):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer
