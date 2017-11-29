from django.views import generic
from .models import BankAccount


class BankAccountListView(generic.ListView):
    model = BankAccount

    def get_queryset(self):
        return BankAccount.objects.all()