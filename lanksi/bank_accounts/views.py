from django.shortcuts import render
from .models import BankAccount
from django.views import View


class BankAccountListView(View):
    model = BankAccount
    template_name = "bankaccount_list.html"

    def get(self, request):
        if request.user.is_authenticated:
            accounts = BankAccount.objects.filter(owner=request.user)
        else:
            accounts = None
        return render(request, self.template_name, {'accounts': accounts})
