import requests
import json
from config import keys


class ConvertionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):

        if quote == base:
            raise ConvertionException(f'Не возможно перевести одинаковые валюты {base}')
        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')
        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать введенную сумму {amount}')

        r = requests.get(f'https://api.apilayer.com/exchangerates_data/latest?base={base_ticker}&symbols={quote_ticker}',
                         headers={"apikey": "AstXDZSCFkl2OFGaIwlg5vN6v3Ew2qSL"})
        total_base = json.loads(r.content)['rates'][keys[quote]]

        return total_base
