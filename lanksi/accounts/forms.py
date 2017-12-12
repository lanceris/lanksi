from decimal import Decimal

from django.conf import settings
from django import forms
from django.utils.timezone import datetime
from django.utils.translation import ugettext_lazy as _
from dateutil.relativedelta import relativedelta

from accounts.models import BankAccount, Transaction
from categories.models import Category
from accounts.mixins import CategoryMixin, DescriptionMixin, AccountMixin, CommentMixin


class AddBankAccountForm(DescriptionMixin, forms.ModelForm):
    class Meta:
        model = BankAccount
        exclude = ('owner',)

    balance = forms.CharField(max_length=15, initial=Decimal("0"))


class EditBankAccountForm(DescriptionMixin, forms.ModelForm):
    label = forms.CharField()

    class Meta:
        model = BankAccount
        exclude = ('owner', 'balance', 'currency')


class TransactionForm(CommentMixin, CategoryMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.cat_type = kwargs.pop('cat_type')
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(owner=self.request.user)\
                                                           .filter(cat_type=self.cat_type)

    class Meta:
        model = Transaction
        fields = ('amount', 'category', 'tr_tags')

    amount = forms.DecimalField(max_digits=12,
                                decimal_places=2,
                                min_value=0,
                                label=_("Amount"))


class MoveMoneyForm(AccountMixin, CommentMixin, CategoryMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.acc = kwargs.pop('account')
        self.cat_type = kwargs.pop('cat_type')
        super(MoveMoneyForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(owner=self.request.user)\
                                                             .filter(currency=self.acc.currency)\
                                                             .exclude(slug=self.acc.slug)
        self.fields['category'].queryset = Category.objects.filter(owner=self.request.user) \
                                                           .filter(cat_type=self.cat_type)

    class Meta:
        model = Transaction
        fields = ('account', 'amount', 'category', 'tr_tags', 'comment')

    amount = forms.DecimalField(max_digits=12,
                                decimal_places=2,
                                min_value=0,
                                label=_("Amount"))


class ExchangeForm(CommentMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.acc = kwargs.pop('account')
        self.cat_type = kwargs.pop('cat_type')
        super(ExchangeForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(owner=self.acc.owner) \
                                                           .filter(cat_type=self.cat_type)
        self.fields['tr_from'].queryset = BankAccount.objects.filter(owner=self.acc.owner)
        self.fields['tr_from'].initial = BankAccount.objects.filter(owner=self.acc.owner).first()
        self.fields['tr_to'].queryset = BankAccount.objects.filter(owner=self.acc.owner)\
                                                           .exclude(currency=self.acc.currency)

    class Meta:
        model = Transaction
        fields = ('tr_from', 'tr_to', 'category', 'comment', 'tr_tags')

    tr_from = forms.ModelChoiceField(queryset=None, disabled=True)
    tr_to = forms.ModelChoiceField(queryset=None)
    amount = forms.DecimalField(max_digits=12,
                                decimal_places=2,
                                min_value=0,
                                label=_("Amount"))


class FilterHistoryForm(AccountMixin, CategoryMixin, forms.Form):
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
        (day, _('Day')),
        (week, _('Week')),
        (month, _('Month')),
        (year, _('Year')),
    )
    time_period = forms.ChoiceField(choices=time_periods,
                                    initial=time_periods[0],
                                    required=False,
                                    label=_("Time period"))
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=years),
                                required=False,
                                label=_("From"))
    date_to = forms.DateField(widget=forms.SelectDateWidget(years=years),
                              required=False,
                              label=_("To"))
    keywords = forms.CharField(required=False,
                               label=_("Keywords"))
    account = forms.ModelChoiceField(queryset=None,
                                     required=False,
                                     label=_("Account"))


