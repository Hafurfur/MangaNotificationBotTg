from pathlib import Path

from requests import get
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from src.logger.base_logger import log


def get_photo_account(acc_id: str, photo_id: str) -> bytes:
    log.info('Поиск аватарки манга аккаунта')
    log.debug(f'{__name__}(acc_id={acc_id}, photo_id={photo_id})')

    try:
        if photo_id == '0':
            response = get('https://cover.imglib.info/uploads/users/placeholder.png')
        else:
            response = get(f'https://mangalib.me/uploads/users/{acc_id}/{photo_id}')
        response.raise_for_status()
    except (HTTPError, ConnectionError, Timeout, RequestException) as error:
        log.error('Ошибка при получении аватара манга аккаунта (requests)', exc_info=error)
        return _get_placeholder_avatar()
    except Exception as error:
        log.error('Ошибка при получении аватара манга аккаунта', exc_info=error)
        return _get_placeholder_avatar()

    log.debug(f'Аватарка манга аккаунта={response.content}')
    return response.content


def _get_placeholder_avatar() -> bytes:
    log.debug(f'{__name__}(получение заглушки аватара манга аккаунта)')

    placeholder_path = Path.joinpath(Path.cwd(), r'.\data\images\placeholder_avatar.png')

    with open(placeholder_path, 'rb') as fr:
        return fr.read()


def _pars_name_acc(row_name: str) -> str:
    log.debug(f'{__name__}(row_name={row_name})')

    split_row_name = row_name.split(' ', 1)
    result = '' if len(split_row_name) < 2 else split_row_name[1].strip(' ')

    log.debug(f'Имя аккаунта={result}')

    return result


def search_account(row_name: str) -> dict:
    log.debug(f'{__name__}(row_name={row_name})')

    name_acc = _pars_name_acc(row_name)

    if not name_acc:
        return {}

    try:
        request_url = f'https://mangalib.me/search?type=user&q={name_acc}'
        response = get(request_url)
        response.raise_for_status()
    except (HTTPError, ConnectionError, Timeout, RequestException) as error:
        log.error('Ошибка при получении манга аккаунта через requests', exc_info=error)
        return {}
    except Exception as error:
        log.error('Ошибка при получении манга аккаунта', exc_info=error)
        return {}

    result = response.json()
    log.debug(f'Данные аккаунта ={result}')

    return result


def get_readable_mg_acc(account_id: int) -> tuple[list, set, int]:
    log.info('Получение читаемой манги аккаунта с сайта')
    log.debug(f'{__name__} account_id={account_id}')

    try:
        response = get(f'http://mangalib.me/bookmark/{account_id}')
        response.raise_for_status()
    except (HTTPError, ConnectionError, Timeout, RequestException) as error:
        log.error('Ошибка при получении читаемой манги аккаунта с сайта (requests)', exc_info=error)
        return [], set(), 404
    except Exception as error:
        log.error('Ошибка при получении читаемой манги аккаунта с сайта', exc_info=error)
        return [], set(), 404

    manga_list = response.json()['items']
    manga_id = set()
    readable_manga = []

    for item in manga_list:
        if item['status'] == 1 and item['manga_id'] not in manga_id:
            manga_id.add(item['manga_id'])
            readable_manga.append(item)

    log.debug(f'readable_manga={readable_manga}, manga_id={manga_id}, status_code={response.status_code}')

    return readable_manga, manga_id, response.status_code
