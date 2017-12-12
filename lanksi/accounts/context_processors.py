from accounts.models import BankAccount, ExchangeRate
from accounts.views import get_sums


def get_rates_and_summary(request):
    rates = ExchangeRate.objects.all()
    if request.user.is_authenticated():
        accounts = BankAccount.objects.filter(owner=request.user)
    else:
        accounts = BankAccount.objects.none()
    sums = get_sums(accounts.values('currency', 'balance'))
    return {'rates': rates,
            'accounts': accounts,
            'sums': sums}