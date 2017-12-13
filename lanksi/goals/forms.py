from django import forms
from django.utils.translation import ugettext_lazy as _

from goals.models import Goal
from accounts.models import BankAccount


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        exclude = ('owner', )


class AddMoneyForm(forms.Form):
    class Meta:
        model = Goal

    def __init__(self, *args, **kwargs):
        self.goal = kwargs.pop('goal')
        self.request = kwargs.pop('request')
        super(AddMoneyForm, self).__init__(*args, **kwargs)
        self.fields['acc_from'].queryset = BankAccount.objects.filter(owner=self.request.user)\
                                                              .filter(currency=self.goal.currency)
        self.fields['amount'].max_value = self.goal.get_money_left()

    acc_from = forms.ModelChoiceField(queryset=None, required=True, label=_('Take money from'))
    amount = forms.DecimalField(max_digits=26,
                                decimal_places=2,
                                min_value=0,
                                max_value=None, label=_('Amount'))