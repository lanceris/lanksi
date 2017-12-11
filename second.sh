cd lanksi
./manage.py shell -c "from accounts.tasks import *;get_currency_rates.delay(settings.CURRENCIES)"

python manage.py runserver