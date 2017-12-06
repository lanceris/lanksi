from celery import Celery, shared_task
from celery.schedules import crontab
import requests
from time import sleep
from accounts.models import ExchangeRate

app = Celery('lanksi',
             broker='amqp://',
             backend='amqp://')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(),
        get_currency_rates.s(),
    )


@shared_task
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
            print(r['base'])
            sleep(0.1)
