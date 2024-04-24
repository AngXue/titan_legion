from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from esi.decorators import token_required
from esi.clients import EsiClientProvider
from esi.models import Token
from .scopes import SCOPES_LIST

esi = EsiClientProvider(app_info_text="titan-legion-management-system v0.0.1")


def login_view(request):
    # 如果用户已经登录，重定向到主页
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'titan_main/login.html')


@login_required
@token_required(scopes=SCOPES_LIST)
def home_view(request, token):
    character_id = token.character_id
    required_scopes = ['esi-skills.read_skillqueue.v1']

    # get a token
    token = Token.get_token(character_id, required_scopes)

    # call the endpoint
    notifications = esi.client.Skills.get_characters_character_id_skillqueue(
        character_id=character_id,
        token=token.valid_access_token()
    ).result()

    return render(request, 'titan_main/home.html', {'token': token, 'notifications': notifications})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
