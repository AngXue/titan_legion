import logging

from django.shortcuts import redirect
from esi.clients import EsiClientProvider
from esi.models import Token

logging = logging.getLogger(__name__)
esi = EsiClientProvider(app_info_text="titan-legion-management-system v0.0.1")


def eve_auth_view(request):
    logging.debug(
        "EVE Auth request from %s",
        request.user,
    )
    return redirect('social:begin', 'eveonline')


def get_eve_isk(character_id):
    required_scopes = ['esi-wallet.read_character_wallet.v1']

    token = Token.get_token(character_id, required_scopes)

    notifications = esi.client.Wallet.get_characters_character_id_wallet(
        character_id=character_id,
        token=token.valid_access_token()
    ).result()

    return notifications


def get_eve_skill(character_id):
    required_scopes = ['esi-skills.read_skills.v1']

    token = Token.get_token(character_id, required_scopes)

    notifications = esi.client.Skills.get_characters_character_id_skills(
        character_id=character_id,
        token=token.valid_access_token()
    ).result()

    return notifications
