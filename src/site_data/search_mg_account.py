from requests import get
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


def get_photo_account(acc_id: str, photo_id: str) -> bytes:
    try:
        if photo_id == '0':
            response = get('https://cover.imglib.info/uploads/users/placeholder.png')
        else:
            response = get(f'https://mangalib.me/uploads/users/{acc_id}/{photo_id}')
        response.raise_for_status()
    except (HTTPError, ConnectionError, Timeout, RequestException) as error:
        print(f'Error: {error}')

    return response.content


def _pars_name_acc(text: str) -> str | None:
    res = text.split(' ', 1)
    return None if len(res) < 2 else res[1].strip(' ')


def search_account(text: str) -> dict | None:
    res_parse = _pars_name_acc(text)

    if res_parse:
        request_url = f'https://mangalib.me/search?type=user&q={res_parse}'
    else:
        return None

    try:
        response = get(request_url)
        response.raise_for_status()
    except (HTTPError, ConnectionError, Timeout, RequestException) as error:
        print(f'Error: {error}')

    account_dict = response.json()

    return account_dict if account_dict else None
