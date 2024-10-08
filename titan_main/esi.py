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


def get_eve_killrecords(character_id):
    # TODO: 待测试
    required_scopes = ['esi-killmails.read_killmails.v1']

    token = Token.get_token(character_id, required_scopes)

    hash_id = esi.client.Killmails.get_characters_character_id_killmails_recent(
        character_id=character_id,
        token=token.valid_access_token()
    ).result()

    notifications = []

    for killmail in hash_id:
        tmp = esi.client.Killmails.get_killmails_killmail_id_killmail_hash(
            killmail_id=killmail['killmail_id'],
            killmail_hash=killmail['killmail_hash'],
            token=token.valid_access_token()
        ).result()
        notifications.append(tmp)

    return notifications
