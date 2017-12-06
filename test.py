import requests
from time import sleep
from accounts.models import ExchangeRate
from django.conf import settings


def get_currency_rates(currencies):
    for each in currencies:
        payload = {'base': each[0],
                   'symbols': ",".join([i[0] for i in currencies if i != each[0]])}
        r = requests.get('https://api.fixer.io/latest', params=payload).json()
        for other_currency, value in r['rates'].items():
            ExchangeRate.objects.create(base_currency=r['base'],
                                        other_currency=other_currency,
                                        value=value,
                                        date=r['date'])
            sleep(1)