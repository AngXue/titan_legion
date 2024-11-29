import json
import re
import urllib.parse

import requests

from titan_legion.settings import env


def generate_url(search_value):
    base_url = "https://seat.winterco.space/tools/paptracking"
    params = {
        "draw": "2",
        "columns[0][data]": "character",
        "columns[0][name]": "character",
        "columns[0][searchable]": "true",
        "columns[0][orderable]": "true",
        "columns[0][search][value]": "",
        "columns[0][search][regex]": "false",
        "columns[1][data]": "nickname",
        "columns[1][name]": "nickname",
        "columns[1][searchable]": "false",
        "columns[1][orderable]": "true",
        "columns[1][search][value]": "",
        "columns[1][search][regex]": "false",
        "columns[2][data]": "qq_id",
        "columns[2][name]": "qq_id",
        "columns[2][searchable]": "false",
        "columns[2][orderable]": "true",
        "columns[2][search][value]": "",
        "columns[2][search][regex]": "false",
        "columns[3][data]": "logoff_date",
        "columns[3][name]": "logoff_date",
        "columns[3][searchable]": "false",
        "columns[3][orderable]": "true",
        "columns[3][search][value]": "",
        "columns[3][search][regex]": "false",
        "columns[4][data]": "character_count",
        "columns[4][name]": "character_count",
        "columns[4][searchable]": "false",
        "columns[4][orderable]": "true",
        "columns[4][search][value]": "",
        "columns[4][search][regex]": "false",
        "columns[5][data]": "pap_count",
        "columns[5][name]": "pap_count",
        "columns[5][searchable]": "false",
        "columns[5][orderable]": "true",
        "columns[5][search][value]": "",
        "columns[5][search][regex]": "false",
        "columns[6][data]": "strat_pap_count",
        "columns[6][name]": "strat_pap_count",
        "columns[6][searchable]": "false",
        "columns[6][orderable]": "true",
        "columns[6][search][value]": "",
        "columns[6][search][regex]": "false",
        "order[0][column]": "5",
        "order[0][dir]": "desc",
        "order[1][column]": "0",
        "order[1][dir]": "asc",
        "start": "0",
        "length": "50",
        "search[value]": search_value,
        "search[regex]": "false",
    }
    encoded_params = urllib.parse.urlencode(params)
    return f"{base_url}?{encoded_params}"


def get_pap(parsed_response):
    extracted_data = [
        {
            'username': re.search(r'/> (.+?)\n', item.get('character', '')).group(1) if re.search(r'/> (.+?)\n',
                                                                                                  item.get('character',
                                                                                                           '')) else '',
            'pap_count': item.get('pap_count', '')
        }
        for item in parsed_response.get('data', [])
    ]
    return extracted_data[0]['pap_count'] if extracted_data else 0


def get_legion_pap(username, headers=None, cookies=None):
    url = generate_url(username)

    if cookies is None:
        cookies = {
            'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': env('SEAT_REMEMBER_TOKEN'),
            'cf_clearance': env('SEAT_CF_CLEARANCE'),
            'XSRF-TOKEN': env('SEAT_XSRF_TOKEN'),
            'laravel_session': env('SEAT_LARAVEL_SESSION'),
        }
    cookie = ''.join([f"{key}={value}; " for key, value in cookies.items()])

    if headers is None:
        headers = {
            'x-csrf-token': env('SEAT_CSRF_TOKEN'),
            'x-requested-with': 'XMLHttpRequest',
            'cookie': cookie,
        }

    response = requests.get(url, headers=headers)
    parsed_response = json.loads(response.content)
    return get_pap(parsed_response)
