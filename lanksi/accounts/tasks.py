import requests
from accounts.models import ExchangeRate
from time import sleep
from celery import task
from lanksi.celery import app
from celery.utils.log import get_task_logger
from django.conf import settings
from celery.schedules import crontab

logger = get_task_logger(__name__)

app.conf.beat_schedule = {
    'update_rates_everyday': {
        'task': 'accounts.tasks.get_currency_rates',
        'schedule': crontab(0, 0), # Update every midnight
        'args': (settings.CURRENCIES,)
    }
}

@task
def get_currency_rates(currencies):
    logger.info('Getting currency rates')
    ExchangeRate.objects.all().delete()
    for each in currencies:
        payload = {'base': each[0],
                   'symbols': ",".join([i[0] for i in currencies if i != each[0]])}
        r = requests.get('https://api.fixer.io/latest', params=payload).json()
        for other_currency, value in r['rates'].items():
            ExchangeRate.objects.create(base_currency=r['base'],
                                        other_currency=other_currency,
                                        value=value,
                                        date=r['date'])
            sleep(0.5)
