from django import forms
from .models import BankAccount, Transaction, TR_TAG_CHOICES
from datetime import datetime


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        exclude = ('owner',)

    balance = forms.CharField(max_length=15)


class BankAccountEditForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        exclude = ('owner', 'balance', 'currency')


class TransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    tag = forms.IntegerField(widget=forms.Select(choices=TR_TAG_CHOICES), required=False)
    description = forms.CharField(widget=forms.Textarea(), required=False)


class MoveMoneyForm(forms.Form):

    account = forms.ModelChoiceField(queryset=BankAccount.objects.all())
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    tag = forms.IntegerField(widget=forms.Select(choices=TR_TAG_CHOICES), required=False)
    description = forms.CharField(widget=forms.Textarea(), required=False)


class FilterHistoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(FilterHistoryForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(owner=self.request.user)

    years = [year for year in range(1985, datetime.today().year + 1)][::-1]
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=years), required=False)
    date_to = forms.DateField(widget=forms.SelectDateWidget(years=years), required=False)
    keywords = forms.CharField(required=False)
    account = forms.ModelChoiceField(queryset=None, required=False)
