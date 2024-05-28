import json
import re

import requests


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
        "columns[1][data]": "character_count",
        "columns[1][name]": "character_count",
        "columns[1][searchable]": "false",
        "columns[1][orderable]": "true",
        "columns[1][search][value]": "",
        "columns[1][search][regex]": "false",
        "columns[2][data]": "pap_count",
        "columns[2][name]": "pap_count",
        "columns[2][searchable]": "false",
        "columns[2][orderable]": "true",
        "columns[2][search][value]": "",
        "columns[2][search][regex]": "false",
        "columns[3][data]": "strat_pap_count",
        "columns[3][name]": "strat_pap_count",
        "columns[3][searchable]": "false",
        "columns[3][orderable]": "true",
        "columns[3][search][value]": "",
        "columns[3][search][regex]": "false",
        "order[0][column]": "2",
        "order[0][dir]": "desc",
        "start": "0",
        "length": "50",
        "search[value]": search_value,
        "search[regex]": "false",
    }
    # 构建完整的 URL
    url = base_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])
    return url


def get_pap(parsed_response):
    extracted_data = []

    # 检查data是否为空
    if 'data' in parsed_response:
        # 遍历每个项目
        for item in parsed_response['data']:
            # 提取 username 和 pap_count
            character = item.get('character', '')
            pap_count = item.get('pap_count', '')

            # 提取用户名
            match = re.search(r'/> (.+?)\n', character)
            if match:
                username = match.group(1)
            else:
                username = ''

            # 添加提取的数据到列表中
            extracted_data.append({'username': username, 'pap_count': pap_count})

    if not extracted_data:
        return 0
    return extracted_data[0]['pap_count']


def get_legion_pap(username, headers=None, cookies=None):
    # 请求的 URL
    url = generate_url(username)

    # 请求头
    if headers is None:
        headers = {
            "X-Requested-With": "XMLHttpRequest"
        }

    # 请求的 Cookie
    if cookies is None:
        cookies = {
            "_ga": "GA1.1.661646371.1715068983",
            "cf_clearance": "Nr3zBaYVeIBKLrgsm76MwVP8sNQ7MKHQkWdCInzlZo4-1715068983-1.0.1.1-TZlsRxCAYcmrw9dc3JwAgxv78bu5058nDte4oZ4ag9rf7cO9x9vgdqHevf5dhpXLHi_1iS7IWCTuYUzjbSzySA",
            "remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d": "eyJpdiI6IjhCc0djeDhnTHRuVlwvY2FDTHFjM3ZBPT0iLCJ2YWx1ZSI6InpVQWR4Q1MxdmF6eFhwdmFkVkZXTm1WaFp0Z2ZISDJkczZkR3QzTXg2N2Vjd3BPK2F0SER0cElvTlNHQ0QxQUtwSU1aeXIzdjZWeTBxdkNKa0gyYTBRRjQ2dUxFdnlpK3RjQzkrRlwvMUI2WEtDbFdLYVwvV1krRVMxOVJEaXBRUFNDejNycUZLZ3ZUREdXZ2hBXC9GZVJ0R0FLQzNVV1B4YWU2bFF6bXdFS1Nwbz0iLCJtYWMiOiI4ZDBkYTY4NWFkNGJmMzM4OTlkOGYyNzEzNTdjN2NmOTc5NDc4NTQ3MmRmODlhODc5OTVlOTNiNzM2ODhkYTFhIn0%3D",
            "_ga_2SL951BRN5": "GS1.1.1716130814.5.1.1716131631.60.0.0",
            "XSRF-TOKEN": "eyJpdiI6ImRERGdaYytLQUUzU2swVWFlVWgxOVE9PSIsInZhbHVlIjoibXhaYno1YXhSZkIyTDA0S2QyMXdyN2ZZTlEwTVRDMVRKZUFySTZyNFZ3aUlOanROaCt0WVBkZUx0UHpqeWQ4aiIsIm1hYyI6Ijg0ZjNiZTA5YTBkODc2MDViM2UxMjAwMDAwYjFkZWU0MTg2YjNkMzU4YjQxMDQyMmM5M2MwYTk1OTgwOTllMjMifQ%3D%3D",
            "laravel_session": "eyJpdiI6InY5WjFyXC82MXY3MGJBYVJwSnBJMU53PT0iLCJ2YWx1ZSI6IlFxRFJsNlp4aE1JYzhnaWZUM0xUU1Fib0hVVU9pNFgremR1SXYzWm1mYlcyTlJXdHhGanFDOE8zTnlhV3FsVUUzS2RpdnNxeEFBZW9sRlhSMnlZRVhYdkxaWnY5UFd2WDhob1VkY095OVppdVh3T2wrazZUMms1bDJEVzNDdGtYIiwibWFjIjoiYWU5MzVkYzc2Y2U1ZDUzOWU2ZDczZWM5MjQwZWY3ODI3N2MzYTQyZTA1MmJhMzVkZjBjMzE3MTM5MmU0YmM3MCJ9"
        }

    # 发送 GET 请求
    response = requests.get(url, headers=headers, cookies=cookies)

    parsed_response = json.loads(response.content)

    pap = get_pap(parsed_response)

    return pap
