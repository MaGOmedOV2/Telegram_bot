import requests
import json
from config import key


class ConvertionException(Exception):
    pass


class APIException:
    @staticmethod
    def get_price(base: str, quote: str, amound: str):

        if base == quote:
            raise ConvertionException(f'невозможно перевести одинаковые валюты {quote}')

        try:
            first_currency_ticker = key[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            second_currency_ticker = key[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            amound = float(amound)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amound}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={first_currency_ticker}&tsyms={second_currency_ticker}')
        total_base = json.loads(r.content)[key[quote]]

        return total_base