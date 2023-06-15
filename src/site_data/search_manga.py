from requests import get
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


def get_readable_mg_acc(account_id) -> tuple[list, set]:
    try:
        response = get(f'https://mangalib.me/bookmark1111/{account_id}')
        response.raise_for_status()
    except (HTTPError, ConnectionError, Timeout, RequestException) as error:
        print(f'Error: {error}')

    manga_list = response.json()['items']
    manga_id = set()
    readable_manga = []

    for item in manga_list:
        if item['status'] == 1 and item['manga_id'] not in manga_id:
            manga_id.add(item['manga_id'])
            readable_manga.append(item)

    return readable_manga, manga_id


if __name__ == '__main__':
    get_readable_mg_acc('1999511')
