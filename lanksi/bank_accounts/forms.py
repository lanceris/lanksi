from django import forms
from .models import BankAccount, Transaction, TR_TAG_CHOICES


def add_empty_label(choices, empty_label=u''):
    a = list(choices)
    a.insert(0, ('', empty_label))
    return tuple(a)


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        exclude = ('owner',)

    balance = forms.CharField(max_length=42, help_text="Example: USD 100")

    def clean_number(self):
        value = self.cleaned_data['number']
        try:
            BankAccount.objects.get(number=value)
            raise forms.ValidationError("This account number alredy exist.")
        except BankAccount.DoesNotExist:
            return value


class TransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    tag = forms.IntegerField(widget=forms.Select(choices=add_empty_label(TR_TAG_CHOICES)), required=False)
    description = forms.CharField(widget=forms.Textarea())


class MoveMoneyForm(forms.Form):
    def __init__(self, data=None, from_account=None, *arg, **kwarg):
        self.base_fields['account'].queryset = BankAccount.objects \
            .exclude(number__exact=from_account.number)
        super(MoveMoneyForm, self).__init__(data, *arg, **kwarg)

    account = forms.ModelChoiceField(None)
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    tag = forms.IntegerField(widget=forms.Select(choices=add_empty_label(TR_TAG_CHOICES)), required=False)
    description = forms.CharField(widget=forms.Textarea())


class FilterHistoryForm(forms.Form):
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    keywords = forms.CharField(required=False)