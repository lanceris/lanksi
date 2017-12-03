from django import forms
from .models import BankAccount, TR_TAG_CHOICES
from django.utils.timezone import datetime
from dateutil.relativedelta import relativedelta


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
    day = datetime.today() - relativedelta(days=1)
    week = datetime.today() - relativedelta(weeks=1)
    month = datetime.today() - relativedelta(months=1)
    year = datetime.today() - relativedelta(years=1)
    time_periods = (
        (None, ' '),
        (day, 'day'),
        (week, 'week'),
        (month, 'month'),
        (year, 'year'),
    )
    time_period = forms.ChoiceField(choices=time_periods,
                                    initial=time_periods[0],
                                    required=False)
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=years), required=False)
    date_to = forms.DateField(widget=forms.SelectDateWidget(years=years), required=False)
    keywords = forms.CharField(required=False)
    account = forms.ModelChoiceField(queryset=None, required=False)
