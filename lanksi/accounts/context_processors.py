from accounts.models import BankAccount, ExchangeRate
from accounts.views import get_sums
from goals.models import Goal


def get_rates_and_summary(request):
    rates = ExchangeRate.objects.all()
    if request.user.is_authenticated():
        accounts = BankAccount.objects.filter(owner=request.user)
        goals = Goal.objects.filter(owner=request.user)
    else:
        accounts = BankAccount.objects.none()
        goals = Goal.objects.none()
    sums = get_sums(accounts.values('currency', 'balance'))
    return {'rates': rates,
            'accounts': accounts,
            'sums': sums,
            'goals': goals}