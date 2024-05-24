from esi.decorators import token_required
from esi.clients import EsiClientProvider
from esi.models import Token
from django.shortcuts import render, redirect
from .scopes import SCOPES_LIST

esi = EsiClientProvider(app_info_text="titan-legion-management-system v0.0.1")


def eve_auth_view(request):
    return redirect('social:begin', 'eveonline')


@token_required(scopes=SCOPES_LIST)
def get_eve_isk(request, token):
    character_id = token.character_id
    required_scopes = ['esi-skills.read_skillqueue.v1']

    token = Token.get_token(character_id, required_scopes)

    notifications = esi.client.Skills.get_characters_character_id_skillqueue(
        character_id=character_id,
        token=token.valid_access_token()
    ).result()

    return notifications, request


@token_required(scopes=SCOPES_LIST)
def get_eve_skill(request, token):
    character_id = token.character_id
    required_scopes = ['esi-skills.read_skillqueue.v1']

    token = Token.get_token(character_id, required_scopes)

    notifications = esi.client.Skills.get_characters_character_id_skillqueue(
        character_id=character_id,
        token=token.valid_access_token()
    ).result()

    return notifications, request
