import requests


class SearchMangaAccount:
    _accounts = None

    def _get_photo_account(self, accounts: dict) -> dict:

        for acc in accounts:
            try:
                if acc['avatar'] == '0':
                    response = requests.get('https://cover.imglib.info/uploads/users/placeholder.png')
                else:
                    response = requests.get(f'https://mangalib.me/uploads/users/{acc["id"]}/{acc["avatar"]}')
                response.raise_for_status()
                acc['avatar'] = response.content

            except requests.exceptions.HTTPError as error:
                print(f'HTTP error: {error}')
            except requests.exceptions.ConnectionError as error:
                print(f'Connection error: {error}')
            except requests.exceptions.Timeout as error:
                print(f'Timeout error: {error}')
            except requests.exceptions.RequestException as error:
                print(f'Unknown error: {error}')
        return accounts

    def _pars_name_acc(self, text: str) -> str | None:
        res = text.split(' ', 1)
        if len(res) < 2:
            return None
        else:
            return res[1].strip(' ')

    def search_account(self, text: str) -> dict | None:
        res_parse = self._pars_name_acc(text)

        if res_parse:
            request_url = f'https://mangalib.me/search?type=user&q={res_parse}'
        else:
            return None

        try:
            response = requests.get(request_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f'HTTP error: {error}')
        except requests.exceptions.ConnectionError as error:
            print(f'Connection error: {error}')
        except requests.exceptions.Timeout as error:
            print(f'Timeout error: {error}')
        except requests.exceptions.RequestException as error:
            print(f'Unknown error: {error}')

        account_dict = response.json()

        if account_dict:
            return self._get_photo_account(account_dict)
        else:
            return None
