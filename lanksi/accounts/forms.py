from django import forms
from accounts.models import BankAccount
from categories.models import Category
from django.utils.timezone import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal


class AddBankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        exclude = ('owner',)

    balance = forms.CharField(max_length=15, initial=Decimal("0"))


class EditBankAccountForm(forms.ModelForm):
    label = forms.CharField(required=False)

    class Meta:
        model = BankAccount
        exclude = ('owner', 'balance', 'currency')


class TransactionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.cat_type = kwargs.pop('cat_type')
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(owner=self.request.user)\
                                                           .filter(cat_type=self.cat_type)

    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    tag = forms.IntegerField(widget=forms.Select(), required=False)
    category = forms.ModelChoiceField(queryset=None, required=False)
    description = forms.CharField(widget=forms.Textarea(), required=False)


class MoveMoneyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.acc = kwargs.pop('account')
        super(MoveMoneyForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(owner=self.request.user)\
                                                             .exclude(slug=self.acc.slug)
        self.fields['category'].queryset = Category.objects.filter(owner=self.request.user) \
                                                           .filter(cat_type=self.cat_type)

    account = forms.ModelChoiceField(queryset=None)
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    tag = forms.IntegerField(widget=forms.Select(), required=False)
    category = forms.ModelChoiceField(queryset=None, required=False)
    description = forms.CharField(widget=forms.Textarea(), required=False)


class FilterHistoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(FilterHistoryForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(owner=self.request.user)
        self.fields['category'].queryset = Category.objects.filter(owner=self.request.user)

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
    category = forms.ModelChoiceField(queryset=None, required=False)
